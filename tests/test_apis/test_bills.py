from tests.factories import BillFactory, SubBillFactory


def test_create_bill_with_sub_bills(client):
    data = {
        "total": 3,
        "sub_bills": [
            {"amount": 1, "reference": "REF-1"},
            {"amount": 2, "reference": "ref-2"},
        ],
    }

    # Make the POST request to create a bill
    response = client.post("/api/bills/", json=data)
    assert response.status_code == 200
    assert response.json()["message"] == "Bill created successfully"
    assert "data" in response.json()
    assert "id" in response.json()["data"]
    assert response.json()["data"]["total"] == 3
    assert "sub_bills" in response.json()["data"]
    assert len(response.json()["data"]["sub_bills"]) == 2


def test_get_bills_with_sub_bills(client):
    bill1 = BillFactory(total=3)
    SubBillFactory.create(amount=1, reference="REF-1", bill=bill1)
    SubBillFactory.create(amount=2, reference="ref-2", bill=bill1)

    bill2 = BillFactory(total=1)
    SubBillFactory.create(amount=1, reference="INV-1", bill=bill2)

    # Case-1
    # Make the GET request to retrieve all bills
    response = client.get("/api/bills/")
    assert response.status_code == 200

    # Assert the response data against the expected output
    expected_output = [
        {
            "id": 1,
            "total": 3,
            "sub_bills": [
                {"amount": 1, "reference": "REF-1"},
                {"amount": 2, "reference": "ref-2"},
            ],
        },
        {
            "id": 2,
            "total": 1,
            "sub_bills": [{"amount": 1, "reference": "INV-1"}],
        },
    ]
    assert response.json()["data"]["bills"] == expected_output

    # Case-2
    # Make the GET request to retrieve bills filtered by reference "ref-1"
    response = client.get("/api/bills", params={"reference": "ref-1"})
    assert response.status_code == 200

    # Assert the response data against the expected output
    expected_output = [
        {
            "id": 1,
            "total": 3,
            "sub_bills": [{"amount": 1, "reference": "REF-1"}],
        }
    ]
    assert response.json()["data"]["bills"] == expected_output

    # Case-3
    # Make the GET request to retrieve bills filtered by reference "ref"
    response = client.get("/api/bills", params={"reference": "ref"})
    assert response.status_code == 200

    # Assert the response data against the expected output
    expected_output = [
        {
            "id": 1,
            "total": 3,
            "sub_bills": [
                {"amount": 1, "reference": "REF-1"},
                {"amount": 2, "reference": "ref-2"},
            ],
        }
    ]
    assert response.json()["data"]["bills"] == expected_output
    return

    # Case-4
    # Make the GET request to retrieve bills filtered by reference "in"
    response = client.get("/api/bills", params={"reference": "in"})
    assert response.status_code == 200

    # Assert the response data against the expected output
    expected_output = [
        {
            "id": 2,
            "total": 1,
            "sub_bills": [{"amount": 1, "reference": "INV-1"}],
        }
    ]
    assert response.json()["data"]["bills"] == expected_output

    # Case-5
    # Make the GET request to retrieve bills filtered by total_from=3
    response = client.get("/api/bills", params={"total_from": 3})
    assert response.status_code == 200

    # Assert the response data against the expected output
    expected_output = [
        {
            "id": 1,
            "total": 3,
            "sub_bills": [
                {"amount": 1, "reference": "REF-1"},
                {"amount": 2, "reference": "ref-2"},
            ],
        }
    ]
    assert response.json()["data"]["bills"] == expected_output

    # Case-6
    # Make the GET request to retrieve bills filtered by total_from=3
    response = client.get("/api/bills", params={"total_t": 3})
    assert response.status_code == 200

    # Assert the response data against the expected output
    expected_output = [
        {
            "id": 1,
            "total": 3,
            "sub_bills": [
                {"amount": 1, "reference": "REF-1"},
                {"amount": 2, "reference": "ref-2"},
            ],
        },
        {
            "id": 2,
            "total": 1,
            "sub_bills": [{"amount": 1, "reference": "INV-1"}],
        },
    ]
    assert response.json()["data"]["bills"] == expected_output
