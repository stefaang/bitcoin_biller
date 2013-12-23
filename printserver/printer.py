import cups
import qrcode
from xhtml2pdf import pisa

class Printer():
	def main(self, addr = '13BjVxFnZrFCZAR3e1144cWMWwT3WJBJXa', amount = '0', i = ''):
		print 'Printer - Start'

		# Folders
		base = '/home/pi/server/'
		data = '/home/pi/server/data/'

		# Save receipts here
		pngname = data + i + '.png'
		pdfname = data + i + '.pdf'

		# Generate QR code
		uri = 'bitcoin:' + addr + '?amount=' + amount
		qrcode.make(uri).save(pngname)

		# Load template
		with file('template.html') as f: xhtml = f.read()
		xhtml = xhtml.replace('{{ amount }}', amount);
		xhtml = xhtml.replace('{{ address }}', addr);
		xhtml = xhtml.replace('{{ qr }}', pngname);

		# Fix logging error
		import logging
		class PisaNullHandler(logging.Handler):
		    def emit(self, record):
		        pass
		log = logging.getLogger(__name__)
		log.addHandler(PisaNullHandler())
	
		# Create PDF
		print 'Printer - Create PDF'
		pdf = pisa.CreatePDF(xhtml, file(pdfname, "w"))
		if not pdf.err:
			pdf.dest.close()
				
			# Print PDF
			conn = cups.Connection()
			printers = conn.getPrinters()
			# Use first printer
			printer_name = printers.keys()[0]
			print 'Printer - Print with ' + printer_name
		#	conn.printFile(printer_name, pdfname, "Python_Status_print", {})
		else:
			print "Unable to create pdf file"


if __name__=="__main__":
	main()
