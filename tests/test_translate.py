import unittest

from translate import AzureOpenAITranslate

SIMPLE_FINNISH_TEXT_FILE = "./tests/simple_finnish.txt"
SIMPLE_FINNISH_TEXT_TRANSLATION = "Fortum wants subsidies for nuclear power – the minister is generous, the researcher condemns."

class TestAzureOpenAITranslate(unittest.TestCase):

    def test_simple_translation(self):
        '''Simple finnish translation test '''

        # perform the translation
        tr = AzureOpenAITranslate()
        file_contents = tr.read_file(SIMPLE_FINNISH_TEXT_FILE)
        translation = tr.translate(file_contents)

        # verify from LLM if the translations are similar
        _prompt = self._similarity_prompt(translation, SIMPLE_FINNISH_TEXT_TRANSLATION)
        print(_prompt)
        output = tr.chat(_prompt)
        self.assertEqual(
            output.lower(),
            'yes'
        )
    
    def _similarity_prompt(self, actual, expected):
        
        return f'''
        Please check if meaning of below 2 sentences are same and reply only yes or no

        1. {actual}
        2. {expected}
        '''
