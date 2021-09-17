from .i_resource import IResource


class ILoader(IResource):

    # @must_be_implemented(error_msg="Loader должен уметь загружать ресурс")
    def _load(self):
        pass

    # @must_be_implemented(error_msg="Loader должен уметь выгружать ресурс")
    def _upload(self):
        pass

    def _update(self):
        pass
