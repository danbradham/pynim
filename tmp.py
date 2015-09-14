import pynim

pynim.configure(
    hostname='ny-nim',
    port=80)


dan = pynim.User.find_one(username='dan')
print repr(dan)
vitra = dan.get_job(jobname='VITRA_VR')
print repr(vitra)
assets = vitra.get_assets()[0]
print assets

active_projects = pynim.Server.find_one(server='Active_Projects')

print vitra.get_path('asset')
