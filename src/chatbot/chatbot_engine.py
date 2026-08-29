from src.chatbot.conversation import ConversationState
from src.chatbot.intent import detect_intent
from src.chatbot.questions import next_question
from src.chatbot.validator import convert_value, validate_value
from src.chatbot.response_formatter import format_prediction_response
from src.chatbot.conversation_commands import is_exit_command
from src.prediction_engine import predict_health

# Gemini
from backend.services.gemini_service import extract_health_data


# ============================================================
# INTENT MAPPING
# ============================================================

INTENT_MAPPING = {
    "diabetes": "diabetes",
    "heart_disease": "heart",
    "heart": "heart",
    "treatment": "treatment",
}


# ============================================================
# CONDITION-SPECIFIC FIELD MAPPING
# IMPORTANT:
# Same field name ko globally map nahi karna hai.
# ============================================================

FIELD_MAPPING = {

    # --------------------------------------------------------
    # DIABETES
    # --------------------------------------------------------
    "diabetes": {
        "hba1c_level": "HbA1c_level",
        "HbA1c_level": "HbA1c_level",

        "gender": "gender",
        "age": "age",
        "bmi": "bmi",
        "blood_glucose_level": "blood_glucose_level",
        "smoking_history": "smoking_history",
        "hypertension": "hypertension",
        "heart_disease": "heart_disease",
    },

    # --------------------------------------------------------
    # HEART
    # --------------------------------------------------------
    "heart": {
        "age": "age",

        # Gemini gender de to model mein sex
        "gender": "sex",

        "sex": "sex",

        "chest_pain_type": "chest pain type",
        "chest pain type": "chest pain type",

        "resting_bp_s": "resting bp s",
        "resting bp s": "resting bp s",

        "cholesterol": "cholesterol",

        "fasting_blood_sugar": "fasting blood sugar",
        "fasting blood sugar": "fasting blood sugar",

        "resting_ecg": "resting ecg",
        "resting ecg": "resting ecg",

        "max_heart_rate": "max heart rate",
        "max heart rate": "max heart rate",

        "exercise_angina": "exercise angina",
        "exercise angina": "exercise angina",

        "oldpeak": "oldpeak",

        "st_slope": "ST slope",
        "ST slope": "ST slope",
    },

    # --------------------------------------------------------
    # TREATMENT
    # --------------------------------------------------------
    "treatment": {
        "age": "Age",
        "Age": "Age",

        "gender": "Gender",
        "Gender": "Gender",

        "self_employed": "self_employed",
        "family_history": "family_history",
        "work_interfere": "work_interfere",
        "no_employees": "no_employees",
        "remote_work": "remote_work",
        "tech_company": "tech_company",
        "benefits": "benefits",
        "care_options": "care_options",
        "wellness_program": "wellness_program",
        "seek_help": "seek_help",
        "anonymity": "anonymity",
        "leave": "leave",

        "mental_health_consequence": "mental_health_consequence",
        "phys_health_consequence": "phys_health_consequence",

        "coworkers": "coworkers",
        "supervisor": "supervisor",

        "mental_health_interview": "mental_health_interview",
        "phys_health_interview": "phys_health_interview",

        "mental_vs_physical": "mental_vs_physical",

        "obs_consequence": "obs_consequence",

        "country": "country",
        "Country": "country",
    },
}


class ChatbotEngine:

    # ========================================================
    # INIT
    # ========================================================

    def __init__(self):
        self.state = ConversationState()

    # ========================================================
    # RUN PREDICTION
    # ========================================================

    def run_prediction(self):

        result = predict_health(
            self.state.condition,
            self.state.data
        )

        return format_prediction_response(
            self.state.condition,
            result
        )

    # ========================================================
    # GET CANONICAL FIELD
    # ========================================================

    def get_canonical_field(self, field: str):

        condition = self.state.condition

        if condition in FIELD_MAPPING:

            mapping = FIELD_MAPPING[condition]

            return mapping.get(field, field)

        return field

    # ========================================================
    # NORMALIZE ANSWER
    # ========================================================

    def normalize_answer(
        self,
        field: str,
        message: str
    ):

        field = self.get_canonical_field(field)

        converted = convert_value(
            field,
            message
        )

        print("\n===== LOCAL ANSWER =====")
        print(f"Field     : {field}")
        print(f"Input     : {message}")
        print(f"Converted : {converted}")
        print(f"Type      : {type(converted)}")

        return converted

    # ========================================================
    # NORMALIZE GEMINI VALUE
    # ========================================================

    def normalize_gemini_value(
        self,
        field: str,
        value,
        original_field: str = None
    ):

        # ----------------------------------------------------
        # `field` yahan already canonical hota hai (save_gemini_data
        # isse pehle hi map kar chuka hota hai), isliye dobara
        # get_canonical_field() call nahi karte — warna future mein
        # agar mapping idempotent na rahi, to galat field pe map ho
        # sakta tha, aur debug logs mein bhi "original field" galat
        # dikhta.
        #
        # `original_field` sirf debug logging ke liye hai (Gemini ne
        # jo field name diya tha).
        # ----------------------------------------------------

        canonical_field = field

        if original_field is None:
            original_field = field

        # ----------------------------------------------------
        # Value already None
        # ----------------------------------------------------

        if value is None:
            return None

        # ----------------------------------------------------
        # Convert everything through validator
        # This handles:
        #
        # "one"
        # "ek"
        # "type 1"
        # "chest pain type ek hai"
        # "yes"
        # "no"
        # etc.
        # ----------------------------------------------------

        try:

            converted = convert_value(
                canonical_field,
                str(value)
            )

        except Exception as e:

            print(
                f"\nNormalization error for {field}: {e}"
            )

            return value

        print(
            "\n===== GEMINI VALUE NORMALIZATION ====="
        )

        print(
            f"Original field : {original_field}"
        )

        print(
            f"Canonical field: {canonical_field}"
        )

        print(
            f"Original value : {value}"
        )

        print(
            f"Converted value : {converted}"
        )

        return converted

    # ========================================================
    # SAVE GEMINI DATA
    # ========================================================

    def save_gemini_data(
        self,
        health_data: dict
    ):

        for field, value in health_data.items():

            # ------------------------------------------------
            # Convert field name according to condition
            # ------------------------------------------------

            canonical_field = self.get_canonical_field(
                field
            )

            # ------------------------------------------------
            # Normalize value
            # ------------------------------------------------

            converted_value = self.normalize_gemini_value(
                canonical_field,
                value,
                original_field=field
            )

            # ------------------------------------------------
            # Skip None
            # ------------------------------------------------

            if converted_value is None:
                continue

            # ------------------------------------------------
            # Validate
            # ------------------------------------------------

            validation = validate_value(
                canonical_field,
                converted_value
            )

            if not validation["valid"]:

                print(
                    "\n===== GEMINI VALUE INVALID ====="
                )

                print(
                    f"Field : {canonical_field}"
                )

                print(
                    f"Value : {converted_value}"
                )

                print(
                    f"Error : {validation['message']}"
                )

                continue

            # ------------------------------------------------
            # Save
            # ------------------------------------------------

            self.state.add_data(
                canonical_field,
                converted_value
            )

    # ========================================================
    # PROCESS MESSAGE
    # ========================================================

    def process_message(
        self,
        message: str
    ):

        # ====================================================
        # BASIC CLEANING
        # ====================================================

        if message is None:

            return {
                "success": False,
                "message": "Please enter a message."
            }

        message = message.strip()

        if not message:

            return {
                "success": False,
                "message": "Please enter a message."
            }

        # ====================================================
        # STEP 0: EXIT COMMAND
        # ====================================================

        if is_exit_command(message):

            return {
                "success": True,
                "conversation_ended": True,
                "message": (
                    "Conversation ended.\n"
                    "Aap jab chahe naya health assessment "
                    "start kar sakte hain."
                )
            }

        # ====================================================
        # STEP 1: GEMINI EXTRACTION
        # ====================================================

        extraction = None

        try:

            extraction = extract_health_data(
                message=message,
                condition=self.state.condition,
                current_field=self.state.current_field
            )

            print(
                "\n===== GEMINI EXTRACTION ====="
            )

            print(extraction)

        except Exception as e:

            # ------------------------------------------------
            # Gemini error hone par application crash nahi hogi
            # ------------------------------------------------

            print(
                "\n===== GEMINI ERROR ====="
            )

            print(e)

            extraction = None

        # ====================================================
        # STEP 2: DETERMINE CONDITION
        # ====================================================

        if self.state.condition is None:

            condition = "unknown"

            # ------------------------------------------------
            # Gemini se intent mila
            # ------------------------------------------------

            if extraction is not None:

                gemini_intent = getattr(
                    extraction,
                    "intent",
                    "unknown"
                )

                condition = INTENT_MAPPING.get(
                    gemini_intent,
                    "unknown"
                )

            # ------------------------------------------------
            # Gemini fail/unknown
            # fallback keyword detector
            # ------------------------------------------------

            if condition == "unknown":

                condition = detect_intent(
                    message
                )

            # ------------------------------------------------
            # Still unknown
            # ------------------------------------------------

            if condition == "unknown":

                return {
                    "success": False,
                    "message": (
                        "Main Diabetes, Heart Disease "
                        "aur Treatment prediction mein "
                        "help kar sakta hoon."
                    )
                }

            # ------------------------------------------------
            # Save condition
            # ------------------------------------------------

            self.state.set_condition(
                condition
            )

        # ====================================================
        # STEP 3: SAVE GEMINI EXTRACTED DATA
        # ====================================================

        if extraction is not None:

            try:

                health_data = (
                    extraction.health_data.model_dump(
                        exclude_none=True
                    )
                )

            except Exception:

                health_data = {}

            print(
                "\n===== EXTRACTED DATA ====="
            )

            print(health_data)

            # -----------------------------------------------
            # Normalize + validate + save
            # -----------------------------------------------

            self.save_gemini_data(
                health_data
            )

        # ====================================================
        # STEP 4: HANDLE CURRENT QUESTION
        # ====================================================

        current_field = self.state.current_field

        # ----------------------------------------------------
        # BUG FIX: questions.py uses its own field-name spelling
        # (e.g. "chest_pain_type", "age" for treatment) which does
        # NOT always match the canonical training-column name used
        # everywhere else (fields.py, validator.py FIELD_RANGES,
        # the model services) - e.g. heart's canonical name is
        # "chest pain type" (spaced) and treatment's is "Age"
        # (capitalized).
        #
        # The original code validated and stored the answer under
        # the RAW question field name instead of the canonical one.
        # That meant:
        #   - validate_value() silently skipped range/option
        #     checks for every mismatched field (no FIELD_RANGES /
        #     TREATMENT_FIELD_OPTIONS entry existed for the raw name)
        #   - self.state.data ended up with the wrong keys, so the
        #     final predict_heart_dieses()/predict_treatment() calls
        #     KeyError'd on missing "chest pain type" / "Age" / etc.
        #
        # Fix: canonicalize the field name once, and validate/store
        # under that canonical name everywhere.
        # ----------------------------------------------------

        canonical_current_field = None

        if current_field:
            canonical_current_field = self.get_canonical_field(
                current_field
            )

        # ----------------------------------------------------
        # If current question exists and its field is not
        # already saved by Gemini
        # ----------------------------------------------------

        if (
            canonical_current_field
            and canonical_current_field not in self.state.data
        ):

            converted_value = self.normalize_answer(
                current_field,
                message
            )

            # ------------------------------------------------
            # Validation
            # ------------------------------------------------

            validation = validate_value(
                canonical_current_field,
                converted_value
            )

            if not validation["valid"]:

                return {
                    "success": False,
                    "condition": self.state.condition,
                    "data": self.state.data,
                    "message": (
                        f"❌ {validation['message']}"
                    )
                }

            # ------------------------------------------------
            # Save local answer
            # ------------------------------------------------

            self.state.add_data(
                canonical_current_field,
                converted_value
            )

        # ====================================================
        # DEBUG STATE
        # ====================================================

        print(
            "\n===== CONDITION ====="
        )

        print(
            self.state.condition
        )

        print(
            "\n===== CURRENT DATA ====="
        )

        print(
            self.state.data
        )

        # ====================================================
        # STEP 5: NEXT QUESTION
        # ====================================================

        # BUG FIX: pass get_canonical_field so next_question() checks
        # answered-ness using the same canonical keys we now store
        # data under (see STEP 4 fix above and questions.py fix).
        question = next_question(
            self.state.condition,
            self.state.data,
            canonicalize=self.get_canonical_field
        )

        if question:

            next_field = question["field"]

            self.state.set_current_field(
                next_field
            )

            return {
                "success": True,
                "condition": self.state.condition,
                "data": self.state.data,
                "message": question["question"]
            }

        # ====================================================
        # STEP 6: ALL DATA COLLECTED
        # ====================================================

        try:

            prediction_result = self.run_prediction()

            return {
                "success": True,
                "condition": self.state.condition,
                "data": self.state.data,
                "prediction": prediction_result,
                "message": (
                    "Prediction completed successfully."
                )
            }

        except Exception as e:

            print(
                "\n===== PREDICTION ERROR ====="
            )

            print(e)

            return {
                "success": False,
                "condition": self.state.condition,
                "data": self.state.data,
                "message": (
                    "Prediction ke waqt error aaya. "
                    "Please check the collected data "
                    "and prediction model."
                ),
                "error": str(e)
            }