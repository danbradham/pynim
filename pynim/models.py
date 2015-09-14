import requests
import os
from . import make_uri, platform


def first(iterable, **kwargs):
    if not kwargs:
        return iterable

    for item in iterable:
        match = True
        for k, v in kwargs.iteritems():
            value = getattr(item, k, None)
            if value is None or value != v:
                match = False
                break
        if match:
            return item


def encode(dicts, typ):
    return [typ(**d) for d in dicts]


class BaseModel(object):
    '''BaseModel object to be inherited. Subclasses must implement
    the get_uri and __repr__ methods.
    '''

    get_uri = None
    get_info_uri = None
    get_requirements = []

    def __init__(self, **model_data):
        self.__dict__.update(model_data)

    def __str__(self):
        return str(self._id)

    def __eq__(self, other):
        if hasattr(other, '_id'):
            return self._id == other._id
        return False

    def __hash__(self):
        return hash(self._id)

    @property
    def _id(self):
        return self.ID

    @classmethod
    def _find(cls, **kwargs):
        '''Generic Get lookup, reimplement for special cases'''

        r = requests.get(make_uri(cls.get_uri, **kwargs))
        r.raise_for_status()

        data = r.json()

        if not cls.get_info_uri:
            return data

        info_data = []
        for d in data:
            rinfo = requests.get(make_uri(cls.get_info_uri, ID=d['ID']))
            rinfo.raise_for_status()
            info_data.append(rinfo.json()[0])

        return info_data

    @classmethod
    def _validate_params(cls, **kwargs):
        return kwargs.keys() == cls.get_requirements

    @classmethod
    def find(cls, **kwargs):
        cls._validate_params(**kwargs)
        return encode(cls._find(**kwargs), typ=cls)

    @classmethod
    def find_one(cls, **kwargs):
        return first(cls.find(), **kwargs)


class User(BaseModel):
    '''Model representing a NIM User

    usage::

        >> nim_user = pynim.User.find_one(username='nim')
        >> nim_user
        <User>(_id='1', username='nim')
    '''

    get_uri = 'q=getUsers'

    def __repr__(self):
        return '<User>(_id={0}, username={1})'.format(self._id, self.username)

    def get_job(self, **kwargs):
        return Job.find_one(u=self, **kwargs)

    def get_jobs(self):
        return Job.find(u=self)


class Location(BaseModel):
    '''Model representing a NIM Location

    usage::

        >> pynim.Location.find_one(name='test_location')
        <Location>(_id='1', name='test_location')
    '''

    get_uri = 'q=getLocations'

    def __repr__(self):
        return '<Location>(_id={0}, name={1})'.format(self._id, self.name)


class Server(BaseModel):
    '''Model representing a NIM Server

    usage::

        >> pynim.Server.find_one(server='nim_server')
        <Server>(_id='1', server='nim_server')
    '''

    get_uri = 'q=getServers'

    @property
    def root(self):
        if platform == 'win':
            return self.winPath
        if platform == 'osx':
            return self.osxPath
        return self.path

    def __repr__(self):
        r = '<Server>(_id={0}, server={1}, mountpoint={2}, root={3})'
        return r.format(self._id, self.server, self.mountpoint, self.root)


class Job(BaseModel):
    '''Model representing a NIM Job

    usage::

        >> pynim.Job.find(u=nim_user)
        [<Job>(_id=XX, number=XXXXX, jobname=JobName, folder=/path/to/job)...]
    '''

    get_uri = 'q=getUserJobs'
    get_requirements = ['u']
    get_paths_uri = 'q=getPaths'

    def __repr__(self):
        r = '<Job>(_id={0}, number={1}, jobname={2}, folder={3})'
        return r.format(self._id, self.number, self.jobname, self.folder)

    def get_shows(self):
        return Show.find(ID=self)

    def get_show(self, **kwargs):
        return Show.find_one(ID=self, **kwargs)

    def get_assets(self):
        return Asset.find(ID=self)

    def get_asset(self, **kwargs):
        return Asset.find_one(ID=self, **kwargs)

    def get_path(self, pathType, subType=None, server=None):
        '''Return the project path of a specific type.

        :param pathType: job, asset, show, shot'''

        r = requests.get(
            make_uri(self.get_paths_uri, **dict(type=pathType, ID=self)))
        r.raise_for_status()

        paths = r.json()

        if not subType and not server:
            return paths

        if subType:
            path = paths[subType]

        if server:
            path = os.path.join(server.root, path).replace('\\', '/')

        return path

    @classmethod
    def find_one(cls, u, **kwargs):
        return first(cls.find(u=u), **kwargs)


class Show(BaseModel):
    '''Model representing a NIM Show'''

    get_uri = 'q=getShows'
    get_requirements = ['ID']
    get_info_uri = 'q=getShowInfo'

    def __repr__(self):
        r = '<Show>(_id={0}, showname={1}, folder={2}, show_status={3})'
        return r.format(self._id, self.showname, self.folder, self.show_status)

    def get_shots(self):
        return Shot.find(ID=self)

    def get_shot(self, **kwargs):
        return Shot.find_one(ID=self, **kwargs)

    @classmethod
    def find_one(cls, ID, **kwargs):
        return first(cls.find(ID=ID), **kwargs)


class Shot(BaseModel):
    '''Model representing NIM Shot'''

    get_uri = 'q=getShots'
    get_requirements = ['ID']
    get_info_uri = 'q=getShotInfo'

    def __repr__(self):
        r = '<Shot>(shotName={1})'
        return r.format(self.shotName)

    @classmethod
    def find_one(cls, ID, **kwargs):
        return first(cls.find(ID=ID), **kwargs)


class Asset(BaseModel):
    '''Model representing a NIM Asset'''

    get_uri = 'q=getAssets'
    get_requirements = ['ID']
    get_info_uri = 'q=getAssetInfo'
    get_icon_uri = 'q=getAssetIcon'

    def __str__(self):
        '''Asset info command does not return asset id...'''

        return self.__repr__()

    def __repr__(self):
        r = '<Asset>(AMR_path={0}, AMR_filename={1}, assetName={2})'
        return r.format(self.AMR_path, self.AMR_filename, self.assetName)

    def get_icon(self):
        r = requests.get(make_uri(self.get_icon_uri, ID=self))
        r.raise_for_status()

        return r.json()

    @classmethod
    def find_one(cls, ID, **kwargs):
        return first(cls.find(ID=ID), **kwargs)
