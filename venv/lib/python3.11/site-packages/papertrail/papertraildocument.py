from cryptography.fernet import Fernet
from PIL import Image
from fpdf import FPDF, Align
from pdf2image import convert_from_path
import qrcode
from pyzbar.pyzbar import decode
import friendlywords

CHUNK_SIZE = 2143

class PaperTrailDocument:
    def __init__(self, key: bytes, designator: str, document: str, data: bytes = None):
        # Initialize a document with data and Fernet key

        # Initial assignments
        self.document = document
        self.data = data
        self.key = key
        self.designator = designator
        
    def encrypt(self):
        # Encrypt data using key into a document and store in self

        # Encrypt data into Fernet tokens
        chunks = self.__split_data(self.data)
        enc_chunks = [self.__enc_chunk(chunk) for chunk in chunks]

        # Generate the pdf
        pdf = self.__gen_pdf(enc_chunks=enc_chunks)
        
        # Save and return
        pdf.output(self.document)
        
    def decrypt(self):
        # Decrypt document with key into data and store in self
        
        images = self.__get_images()
        chunks = [self.__read_qr_from_image(image) for image in images]
        dec_chunks = [self.__dec_chunk(chunk) for chunk in chunks]
        self.data = b"".join(dec_chunks)

    def get_data(self) -> bytes:
        # Get data if present, if not return an empty bytestring
        return self.data

    def get_document(self) -> str:
        # Get document if present, if not return some sort of null response
        return self.document

    def get_designator(self) -> str:
        # Return user-friendly designator
        return self.designator

    def __gen_qr(self, enc_data: bytes) -> Image:
        qr = qrcode.QRCode(
            version = 40,
            error_correction = qrcode.constants.ERROR_CORRECT_L,
            box_size = 3,
            border = 4,
        )
        qr.add_data(enc_data)
        qrimg = qr.make_image(fill_color = "black", back_color = "white")
        return qrimg.get_image()
        
    def __gen_pdf(self, enc_chunks: list[bytes]) -> FPDF:
        # Initialize PDF and set some parameters
        pdf = FPDF(orientation="portrait", format="letter")
        pdf.set_margin(10)
        pdf.set_text_color(r=76, g=79, b=105)
        # Generate pages
        for i, enc_chunk in enumerate(enc_chunks):
            # Generate the QR code first
            qr_code = self.__gen_qr(enc_chunk)
            # Add a new page to the PDF
            pdf.add_page()
            # Add the header
            pdf.set_font('courier', size=18)
            pdf.multi_cell(
                text=f"PaperTrail Document\n**{self.designator.title()}**\n",
                w=0,
                border=0,
                fill=False,
                markdown=True,
                align='L'
            )
            # Add the image of the QR code
            pdf.image(
                qr_code,
                w=pdf.epw,
                x=Align.C
            )
            # Add the footer
            pdf.set_font('courier', size=14)
            pdf.multi_cell(
                text=f"\nPage **{i+1}/{len(enc_chunks)}**",
                w=pdf.epw,
                border=0,
                markdown=True,
                align='R'
            )
        # Return
        return pdf

    def __split_data(self, data: bytes) -> list[bytes]:
        chunks = [bytes(data[i:CHUNK_SIZE+i]) for i in range(0, len(data), CHUNK_SIZE)]
        return chunks

    def __enc_chunk(self, chunk: bytes) -> bytes:
        fernet = Fernet(self.key)
        enc_chunk = fernet.encrypt(chunk)
        return enc_chunk

    def __dec_chunk(self, chunk:bytes) -> bytes:
        fernet = Fernet(self.key)
        dec_chunk = fernet.decrypt(chunk)
        return dec_chunk

    def __get_images(self) -> list[Image]:
        images = convert_from_path(self.document)
        return images

    def __read_qr_from_image(self, image: Image) -> bytes:
        decoded_qrs = decode(image)
        enc_data = decoded_qrs[0].data
        return enc_data
    
