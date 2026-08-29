def format_prediction_response(condition: str, result: dict):

    condition = condition.lower().strip()

    # DIABETES

    if condition == "diabetes":

        prediction = result.get("prediction")
        probability = result.get("probability_percent", 0)
        risk = result.get("risk_category", "Unknown")

        if prediction == 1:

            message = (
                " Diabetes Assessment Complete\n\n"
                f"Risk Category: {risk}\n"
                f"Estimated Probability: {probability:.2f}%\n\n"
                "Aapke provided information ke basis par "
                "diabetes risk elevated hai. "
                "Kripya healthcare professional se consult karein."
            )

        else:

            message = (
                " Diabetes Assessment Complete\n\n"
                f"Risk Category: {risk}\n"
                f"Estimated Probability: {probability:.2f}%\n\n"
                "Aapke provided information ke basis par "
                "diabetes risk currently low estimate hua hai."
            )

        return {
            "success": True,
            "condition": "diabetes",
            "message": message,
            "prediction": prediction,
            "probability_percent": probability,
            "risk_category": risk,
            "medical_disclaimer": (
                "This prediction is for informational purposes only "
                "and is not a medical diagnosis."
            )
        }


    # HEART DISEASE

    elif condition == "heart":

        prediction = result.get("prediction")
        probability = result.get("probability_percent", 0)
        risk = result.get("risk_category", "Unknown")

        if prediction == 1:

            message = (
                " Heart Disease Assessment Complete\n\n"
                f"Risk Category: {risk}\n"
                f"Estimated Probability: {probability:.2f}%\n\n"
                " Aapke provided information ke basis par "
                "heart disease risk elevated hai. "
                "Kripya healthcare professional se consult karein."
            )

        else:

            message = (
                "Heart Disease Assessment Complete\n\n"
                f"Risk Category: {risk}\n"
                f"Estimated Probability: {probability:.2f}%\n\n"
                "Aapke provided information ke basis par "
                "heart disease risk currently low estimate hua hai."
            )

        return {
            "success": True,
            "condition": "heart",
            "message": message,
            "prediction": prediction,
            "probability_percent": probability,
            "risk_category": risk,
            "medical_disclaimer": (
                "This prediction is for informational purposes only "
                "and is not a medical diagnosis."
            )
        }


    # TREATMENT

    elif condition == "treatment":

        prediction = result.get("prediction")

        if prediction == 1:

            message = (
                "Treatment Assessment Complete\n\n"
                "Based on the provided information, "
                "treatment/support may be recommended."
            )

        else:

            message = (
                "Treatment Assessment Complete\n\n"
                "Based on the provided information, "
                "treatment may not be indicated by this model."
            )

        return {
            "success": True,
            "condition": "treatment",
            "message": message,
            "prediction": prediction,
            "medical_disclaimer": (
                "This prediction is for informational purposes only "
                "and is not a medical diagnosis."
            )
        }


    # UNKNOWN CONDITION

    else:

        return {
            "success": False,
            "condition": condition,
            "message": "Unsupported health condition."
        }