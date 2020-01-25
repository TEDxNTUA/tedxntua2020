class EnglishAutoSlugField(AutoSlugField):
    def pre_save(self, model_instance, add):
        curr_language = model_instance.get_current_language()
        model_instance.set_current_language('en')
        try:
            value = super().pre_save(model_instance, add)
        except TranslationDoesNotExist:
            value = ''
        model_instance.set_current_language(curr_language)
        return value