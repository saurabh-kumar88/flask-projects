from flask import render_template, abort, request

from . import DosAndDonts



@DosAndDonts.route('/DosAndDonts')
def DosAndDonts():
    return render_template("/DosAndDonts/DosAndDonts.html")