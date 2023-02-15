import json
import os
from pathlib import Path


class MemoryFileFactory:

    def __init__(self):
        self._creators = {}

    def register_fileType(self, fileType, creator):
        self._creators[fileType] = creator

    def get_fileCreator(self, format):
        creator = self._creators.get(format)
        if not creator:
            raise ValueError(format)
        return creator()


class FileCreator:
    def create(self, memoryFile, fileType):
        specific_creator = factory.get_fileCreator(fileType)
        memoryFile.initialize(specific_creator)
        specific_creator.createFile()


class JSON_memoryfile_creator:
    def __init__(self):
        pass

    def getDetails(self, filepath, columns):
        self.filepath = filepath
        self.columns = columns

    def createFile(self):
        targetFile = Path(self.filepath)
        targetFile.touch()


factory = MemoryFileFactory()
factory.register_fileType('.json', JSON_memoryfile_creator)


def initializeFolder(targetPath):
    from os import path

    try:
        if not path.exists(targetPath):
            os.makedirs(targetPath)
    except Exception as e:
        print(e)


class MemoryFile():
    def __init__(self, fileName, filepath, extension, columns):
        self.fileName = fileName
        self.filepath = filepath
        self.extension = extension
        self.columns = columns

    def initialize(self, creator):
        creator.getDetails(self.filepath, self.columns)


class FileHandlerBot:
    thisFile = os.path.dirname(__file__)

    def __init__(self):

        self.fileFactoryCreator = FileCreator()

    def readMemoryFile(self, JSONdecoder):  # JSONdecoder is a function that translates JSON to User_M objects

        file = self.getFileFromFilename('User_Memory')

        if file:
            try:
                with open(file['filepath']) as jUM:
                    memoryfile = json.load(jUM, object_hook=JSONdecoder)
            except:
                memoryfile = []
                print('WARNING: 0 users in memory file! No love can be given.')

            return memoryfile

    def readMemoryFileFromDrive(self):  # JSONdecoder is a function that translates JSON to User_M objects
        JSONdecoder = self.CatalogueEncoderDecoder.decode_catalogue
        self.listOfUserMemory = self.memoryFileHandler.readMemoryFile(JSONdecoder)

    def writeToUserMemory(self, userMemory, JSONencoder, file=None):
        # userMemory is a list of python dictionaries each containing a single user's info

        if not file:
            file = self.getFileFromFilename('User_Memory')['filepath']

        if file:
            with open(file, 'w') as jUM:
                json.dump(userMemory, jUM, cls=JSONencoder, sort_keys=True, indent=4)


class CatalogueEncoderDecoder(json.JSONEncoder):
    def default(self, catalogue):
        if isinstance(catalogue, VideoCatalogue):
            cataDict = {""}
            for categ in catalogue.Categories:
                'Category': categ.name
                'URL'''
                for topic in categ.topics:
                    for video in topic.videoWebElements:

            userDict = {
                '__user__': 'true',

                '0_Handle': us.handle,
                'uid': us.uid,
                'Bio': us.bio,
                'AltName': us.altName,
                'Stats': us.statsDict,
                'StatsTime': us.statsDictTimestamp,
                'Past Names': us.listOfPastNames,

            }
            return userDict
        else:
            return super().default(us)

    def decode_catalogue(dct):
        if "__user__" in dct:
            user = VideoCatalogue(dct['0_Handle'])
            user.populate_overwrite(dct)
            return user
        if 'followers' in dct:
            return


class VideoEncoderDecoder(json.JSONEncoder):



class TopicEncoderDecoder(json.JSONEncoder):


class CategoryEncoderDecoder(json.JSONEncoder):


class Video:
    def __int__(self):
        self.name = ''
        self.url = ''


class Topic:
    def __int__(self):
        self.name = ''
        self.url = ''
        self.videos = []


class Category:
    def __int__(self):
        self.name = ''
        self.url = ''
        self.topics = []


class VideoCatalogue:
    def __init__(self):
        self.Categories = []

    def serializeTo_JSON(self, format=False):
        if not format:
            return json.dumps(self, cls=CatalogueEncoderDecoder)
        return json.dumps(self, cls=CatalogueEncoderDecoder, sort_keys=True, indent=4)
