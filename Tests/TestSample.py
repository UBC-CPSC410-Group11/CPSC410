'''
Created on Nov 17, 2013

@author: ericchu
'''

'''
The sole purpose of this module (TestSample) is testing; it serves as a sample input for testing 
the SourceParser package. The content of this module is irrelevant to our program. However, the structure
serves to yield meaningful test results.
'''

class SampleClass(object):

    def __init__(self):
        '''
        Constructor
        '''
        
    #this is method documentation
    def __new__(cls, name, bases, args):

        # for all handled settings we will take defaults from provided class,
        # apply project settings on it, apply resolved app settings and then
        # instantiate appropriated app settings properties

        new_class = type.__new__(cls, name, bases, args)

        for section_name in cls.handle_settings:

            if hasattr(new_class, section_name):
                # defaults
                section_class = getattr(new_class, section_name)
                section_settings = section_class.settings.__dict__.copy()

                # project settings
                settings_name = section_class.settings_name
                project_settings = getattr(settings_name, {})
                section_settings.update(project_settings)

                # app class settings
                section_settings_name = '%s_settings' % section_name
                class_settings = getattr(new_class, section_settings_name, {})
                class_settings = (
                    class_settings and class_settings.__dict__.copy())
                section_settings.update(class_settings)

                # sanitize settings
                instance_settings = {}
                for key in section_settings:
                    if not key.startswith('_'):
                        instance_settings[key] = section_settings[key]
                del section_settings

                # initialize appropriate app property
                section_instance = section_class(
                    type(section_settings_name, (), instance_settings))
                setattr(new_class, section_name, section_instance)

        return new_class
    
    def __del__(self):
        self.save()

    def load(self):
        self.data = self.storage.get('session', self.key)
        return self.data

    def save(self):
        if self.key:
            self.storage.put('session', self.key, self.data)
        else:
            raise KeyError('No session key defined. Deleted session?')
    
    


class SampleClass2(object):
    """
    Base for all abstract base classes to be used as settings sections.
    """

    def __init__(self, settings, *args, **kwargs):
        """
        All subclasses MUST call super(…).__init__ when overriding this method.
        """
        self.settings = settings
        
        def put(self, tag, key, obj):
            if isinstance(obj, dict):
                obj_to_save = obj
                obj_to_save['_id'] = key
            else:
                obj_to_save = {}
                obj_to_save['_id'] = key

                self.db[tag].save(obj_to_save)
                
    '''these are comments
    these are comments
    these are comments''' 
               
    def delete(self, tag, key):
        self.db[tag].remove(key)

    def get_free_key(self, tag):
        return self.db[tag].save({})

    # this is a comment
    # this is another comment
    def get_dataset(self, tag):
        '''fdsfdsfds'''
        self.db[tag].find()
        #dsfdsgsjgirwjkfdsjk;
        return 
