import zipfile
import io
from PIL import Image, PngImagePlugin



class DocumentImage:
    """Image of the document"""

    def __init__(self, image: zipfile.ZipExtFile):
        self.zip_image = image
        self.name = self.zip_image.name
        self.image = Image.open(io.BytesIO(self.zip_image.read()))

    def add_watermark(self, watermark: PngImagePlugin.PngImageFile) -> Image.Image:
        """Blends the watermark with the image"""

        self.image = Image.blend(self.image, watermark.resize(self.image.size), alpha=.3)
        return self.image

    def to_bytes(self) -> bytes:
        """Returns the image as bytes"""

        img_bytes = io.BytesIO()
        self.image.save(img_bytes, format=self.name.split(".")[-1].upper())

        return img_bytes.getvalue()


class DocumentWatermarker:
    """Watermarks a document

    Args:
        file_path: path to the document
        watermark_path: path to the watermark
        output_file_path: path to the output file (if not specified, the document will be overwritten)
    """

    def __init__(
            self,
            file_path: str,
            watermark_path: str,
            output_file_path=None
    ):
        self.file_path = file_path
        if output_file_path is None:
            self.output_file_path = self.file_path
        else:
            self.output_file_path = output_file_path

        # the docx file is a ZIP archive so we can open it as a zip
        self.zip_file = zipfile.ZipFile(self.file_path, mode="a")
        self.files = self.get_all_files()
        self.watermark = Image.open(watermark_path)

    def __call__(self, *args, **kwargs):
        self.add_watermarks()

    def get_all_files(self) -> dict:
        """Returns all image files contained in the document"""

        return {
            file: DocumentImage(self.zip_file.open(file))
            # if file is in "word/media/" path (then it is an image)
            if file.startswith("word/media/") else self.zip_file.open(file).read()
            for file in self.zip_file.namelist()
        }

    def add_watermarks(self):
        """Adds watermarks to all images in document"""

        with zipfile.ZipFile(self.output_file_path, 'w') as new_zip:
            for file_name in self.files:
                if file_name.startswith("word/media/"):

                    self.files[file_name].add_watermark(self.watermark)

                    new_zip.writestr(
                        self.files[file_name].name,
                        self.files[file_name].to_bytes()
                    )

                else:
                    new_zip.writestr(
                        file_name,
                        self.files[file_name]
                    )

    def close(self):
        self.zip_file.close()



def watermark_document_images(
        file_path,
        watermark_path,
        output_file_path=None
):
    doc = DocumentWatermarker(
        file_path=file_path,
        watermark_path=watermark_path,
        output_file_path=output_file_path
    )
    doc.add_watermarks()
    doc.close()
