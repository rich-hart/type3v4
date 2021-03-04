from django.apps import AppConfig
from django.db.models.signals import post_migrate, post_save


class TagsConfig(AppConfig):
    name = 'tags'
    def ready(self):
        from tags.signals import (
            save_project_tag,
            save_accociation_tag,
            load_application_space,
            load_namespace,
            load_model_space,
        )
        from tags.models import Project, Association
        post_migrate.connect(load_application_space, sender=self)
        post_migrate.connect(load_namespace, sender=self)
        post_migrate.connect(load_model_space, sender=self)
        post_save.connect(receiver=save_project_tag, sender=Project)
        post_save.connect(receiver=save_accociation_tag, sender=Association)
                       
