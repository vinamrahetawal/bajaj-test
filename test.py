import requests

registration_url = "https://bfhldevapigw.healthrx.co.in/hiring/generateWebhook/PYTHON"
user_details = {
    "name": "Vinamra Hetawal",
    "regNo": "0827CI221152",
    "email": "vinamrahetawal220677@acropolis.in"
}

response = requests.post(registration_url, json=user_details)

if response.status_code == 200:
    print("Registration successful!")
    # Extract JSON response
    data = response.json()
    webhook_url = data.get("webhook")
    access_token = data.get("accessToken")
    print("Webhook URL:", webhook_url)
    print("Access Token:", access_token)
else:
    print(f"Registration failed with status code {response.status_code}")
    print("Response:", response.text)
    exit()

final_sql_query = """
SELECT 
    e1.EMP_ID,
    e1.FIRST_NAME,
    e1.LAST_NAME,
    d.DEPARTMENT_NAME,
    COUNT(e2.EMP_ID) AS YOUNGER_EMPLOYEES_COUNT
FROM 
    EMPLOYEE e1
JOIN 
    DEPARTMENT d ON e1.DEPARTMENT = d.DEPARTMENT_ID
LEFT JOIN 
    EMPLOYEE e2 ON e1.DEPARTMENT = e2.DEPARTMENT 
    AND e2.DOB > e1.DOB 
    AND e1.EMP_ID != e2.EMP_ID  
GROUP BY 
    e1.EMP_ID, e1.FIRST_NAME, e1.LAST_NAME, d.DEPARTMENT_NAME
ORDER BY 
    e1.EMP_ID DESC;
"""

headers = {
    "Authorization": access_token,
    "Content-Type": "application/json"
}

payload = {
    "finalQuery": final_sql_query.strip()
}

response = requests.post(webhook_url, json=payload, headers=headers)

if response.status_code == 200:
    print("SQL query submitted successfully!")
else:
    print("Submission failed.")
    print("Status Code:", response.status_code)
    print("Response:", response.text)