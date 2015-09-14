from nose.tools import ok_, eq_, raises, with_setup
import pynim
pynim.configure(hostname='ny-nim')


def test_get_nim_root_user():

    users = pynim.User.find()
    nim_user = pynim.User.find_one(username='nim')
    ok_(nim_user in users)

    eq_(nim_user.username, 'nim')
    eq_(nim_user._id, '1')
    eq_(nim_user.first_name, 'NIM')
    eq_(nim_user.last_name, 'ROOT')
    eq_(nim_user.full_name, 'NIM ROOT')


def test_get_jobs_from_user():

    nim_user = pynim.User.find_one(username='nim')
    nim_user_jobs = nim_user.get_jobs()

    eq_(len(nim_user_jobs), 1)


def test_get_assets_from_job():
    nim_user = pynim.User.find_one(username='nim')
    test_job = nim_user.get_job(jobname='TESTING')
    assets = test_job.get_assets()

    names = [asset.assetName for asset in assets]

    eq_(names, ['aAsset', 'bAsset', 'cAsset', 'dAsset'])


def test_get_shows_from_job():
    nim_user = pynim.User.find_one(username='nim')
    test_job = nim_user.get_job(jobname='TESTING')
    shows = test_job.get_shows()

    names = [show.showname for show in shows]

    eq_(names, ['aShow', 'bShow', 'cShow', 'dShow'])


def test_get_shots_from_shows():
    nim_user = pynim.User.find_one(username='nim')
    test_job = nim_user.get_job(jobname='TESTING')
    show = test_job.get_show(showname='aShow')
    shots = show.get_shots()

    names = [shot.shotName for shot in shots]

    eq_(names, ['SH_010', 'SH_020', 'SH_030', 'SH_040'])
