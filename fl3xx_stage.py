import marimo

__generated_with = "0.15.4"
app = marimo.App(width="medium")


@app.cell
def _():
    import requests
    import uuid
    import json
    from pathlib import Path

    API_TOKEN = "RGllGNJdHveuGH9WA-qObLbaicCpazaU"
    BASE_URL = "https://stage.fl3xx.us/api/external"

    ARCHIVE_DIR = Path("quote_archives")

    headers = {
        "X-Auth-Token": API_TOKEN,
        "Content-Type": "application/json",
    }

    def recreate_quote_from_file(path: Path):
        with path.open("r", encoding="utf-8") as f:
            src = json.load(f)

        # Build customer block
        customer = src.get("customer", {})
        account = customer.get("account", {})

        customer_payload = {
            "firstName": customer.get("firstName"),
            "lastName": customer.get("lastName"),
            "logName": customer.get("logName"),
            "salutation": customer.get("salutation"),
            "birthDate": customer.get("birthDate"),
            "status": customer.get("status"),
            "acronym": customer.get("acronym"),
            "account": {
                "name": account.get("name"),
                "phone": account.get("phone"),
                "mobile": account.get("mobile"),
                "vatNumber": account.get("vatNumber"),
                "notes": account.get("notes"),
                "accountNumber": account.get("accountNumber"),
                "accountid": account.get("accountid"),
                "address": account.get("address"),
            },
        }

        # Build legs
        legs_payload = []
        for leg in src.get("legs", []):
            legs_payload.append({
                "aircraft": leg.get("aircraft", src.get("aircraft")),
                "departureAirport": leg.get("departureAirport"),
                "arrivalAirport": leg.get("arrivalAirport"),
                "departureDate": leg.get("departureDate"),
                "departureDateUTC": leg.get("departureDateUTC"),
                "arrivalDate": leg.get("arrivalDate"),
                "arrivalDateUTC": leg.get("arrivalDateUTC"),
                "pax": leg.get("pax"),
                "workflow": leg.get("workflow"),
                "workflowCustomName": leg.get("workflowCustomName"),
                "flightTime": leg.get("flightTime"),
                "blockTime": leg.get("blockTime"),
                "distance": leg.get("distance"),
                "warnings": leg.get("warnings"),
                "status": leg.get("status"),
                "departureAirportObj": leg.get("departureAirportObj"),
                "arrivalAirportObj": leg.get("arrivalAirportObj"),
            })

        price_payload = src.get("price", {})

        payload = {
            "aircraft": src.get("aircraft"),
            "customer": customer_payload,
            "legs": legs_payload,
            "price": price_payload,
            "quotePrice": price_payload,
            "accountPrice": price_payload,
            "comment": src.get("comment"),
            "workflow": src.get("workflow"),
            "workflowCustomName": src.get("workflowCustomName"),
            "origin": src.get("origin"),
            "externalReference": str(uuid.uuid4()),  # always new
        }

        post_url = f"{BASE_URL}/quote"
        resp = requests.post(post_url, json=payload, headers=headers)

        print(f"POST {path.name} → {resp.status_code}")
        print(resp.text)
        print("----")


    if __name__ == "__main__":
        print("Recreating archived quotes...")

        for path in ARCHIVE_DIR.glob("*.json"):
            recreate_quote_from_file(path)

        print("DONE.")

    return


if __name__ == "__main__":
    app.run()
