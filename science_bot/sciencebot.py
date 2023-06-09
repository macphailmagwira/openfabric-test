import random


class ScienceBot:
    def __init__(self, agent, nlp, hash_table, responses, greetings, answer_style):
        
        """
        Initializes the ScienceBot class.

        Parameters:
            agent (object): The Rasa agent used for message parsing.
            nlp (object): The spaCy NLP model used for message processing.
            hash_table (dict): A hash table of subject definitions.
            responses (dict): A dictionary of response messages.
            greetings (list): A list of greeting messages.
            answer_style (list): A list of answer styles.
        """
        
        
        self.agent = agent
        self.nlp = nlp
        self.hash_table = hash_table
        self.responses = responses
        self.greetings = greetings
        self.answer_style = answer_style

    async def _handle_message(self, doc):
        
        """
        Handles the incoming message.

        Parameters:
            doc (str): The message to be processed.

        Returns:
            A list of response messages and definitions.
        """
        
        response = ""
        definition = ""
        output = []

        rasa_response = await self.agent.parse_message(message_data=str(doc))

        if (
            "intent" in rasa_response
            and rasa_response["intent"]
            and "name" in rasa_response["intent"]
            and rasa_response["intent"]["name"]
        ):
            intent_name = rasa_response["intent"]["name"]

            if intent_name == "greet":
                response = str(random.choice(self.greetings))

            elif intent_name == "ask_for_single_definition":
                main_subjects = []

                for token in doc:
                    if token.pos_ == "NOUN":
                        print(token)
                        main_subjects.append(token)

                if len(main_subjects) == 0:
                    response = self.responses["NOT_QUESTION"]
                elif len(main_subjects) == 1:

                    result = await self._get_single_definition(main_subjects[0])

                    if len(str(result)) == 0:
                        response = self.responses["NOT_QUESTION_BUT_SUBJECT"]

                    else:

                        definition = result
                        response = str(random.choice(self.answer_style))

                elif len(main_subjects) > 1:
                    response = self.responses["QUESTION_MORE_THAN_TWO"]
            else:
                response = self.responses["NOT_QUESTION_NOT_SUBJECT_MODEL_ERROR"]
        else:
            response = self.responses["INPUT_MODEL_ERROR"]

        output.append(response)
        output.append(definition) if len(definition) != 0 else output.append("")

        return output

    async def _get_single_definition(self, subject):
        
        """
        Retrieves the definition for a given subject.

        Parameters:
            subject (str): The subject for which to retrieve the definition.

        Returns:
            The definition for the given subject, if it exists in the hash table.
        """

        definition = ""

        try:
            definition = self.hash_table.get(str(subject))
            

        except KeyError:
            definition = ""
            

        return definition
