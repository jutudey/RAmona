SELECT 
    id,
	paymentLink,
    status, 
    merchantReference, 
    ROUND(CAST(REPLACE(amount, 'GBP ', '') AS REAL), 2) AS amount, 
    creationDate,
	createdBy,
    shopperEmail,
    
    CASE
        -- Extract substring between the ":" and the second "-"
        WHEN merchantReference LIKE '%:%-%-%' THEN 
            SUBSTR(
                merchantReference,
                INSTR(merchantReference, ':') + 1,
                INSTR(SUBSTR(merchantReference, INSTR(merchantReference, '-') + 1), '-') + INSTR(merchantReference, '-') - INSTR(merchantReference, ':') - 1
            )
        -- If there's no ":", insert "No invoice reference"
        WHEN merchantReference NOT LIKE '%:%' THEN 'No invoice reference'
        ELSE NULL  -- Catch-all for any other cases
    END AS invoiceReference,

    -- New column to extract 6-character string starting with "10"
    CASE
        -- Check if the string starts with "10", is 6 digits long, and the 6th character is not "-"
        WHEN SUBSTR(merchantReference, INSTR(merchantReference, '10'), 6) LIKE '10____'
             AND SUBSTR(merchantReference, INSTR(merchantReference, '10') + 5, 1) != '-' THEN
            SUBSTR(merchantReference, INSTR(merchantReference, '10'), 6)
        ELSE NULL
    END AS CustomerID,

	    -- New column to extract 6-character string starting with "20"
    CASE
        -- Check if the string starts with "10", is 6 digits long, and the 6th character is not "-"
        WHEN SUBSTR(merchantReference, INSTR(merchantReference, '20'), 6) LIKE '20____'
             AND SUBSTR(merchantReference, INSTR(merchantReference, '20') + 5, 1) != '-' THEN
            SUBSTR(merchantReference, INSTR(merchantReference, '20'), 6)
        ELSE NULL
    END AS PetID
	
	
FROM adyen_PaymentLinks

WHERE 
    amount NOT IN ('GBP 0.01', 'GBP 1.00', 'GBP 0.10')
    AND LENGTH("merchantReference") > 24;
