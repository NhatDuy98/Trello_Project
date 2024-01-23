class CamelCaseConverter:
    def __snake_to_camel(input_str: str) -> str:
        string_split = input_str.split("_")
        return string_split[0] + "".join(word.capitalize() for word in string_split[1:])
    
    @staticmethod
    def to_dto(obj):
        return {CamelCaseConverter.__snake_to_camel(key): getattr(obj, key) for key in obj.__dict__.keys() if not key.startswith('_')}