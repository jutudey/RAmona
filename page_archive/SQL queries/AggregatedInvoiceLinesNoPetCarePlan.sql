CREATE TABLE IF NOT EXISTS PaygInvoices(
	"Invoice #" TEXT, 
    "Invoice Date" TEXT, 
    "Client Contact Code" TEXT, 
    "Last Name" TEXT, 
    "Animal Code" TEXT, 
    "EvPetID" TEXT,
    "Animal Name" TEXT, 
    "PetID" TEXT, 
    "SubscriptionStatus" TEXT,
    "ProductCode" TEXT,
    "ActualEvWp" TEXT,
    Total_Invoiced_Summary REAL
);

DELETE FROM PaygInvoices; 

INSERT INTO PaygInvoices (
	"Invoice #", 
    "Invoice Date", 
    "Client Contact Code", 
    "Last Name", 
    "Animal Code", 
    "EvPetID",
    "Animal Name", 
    "PetID", 
    "SubscriptionStatus",
    "ProductCode",
    "ActualEvWp",
    Total_Invoiced_Summary 
	)

SELECT 
    i."Invoice #", 
    i."Invoice Date", 
    i."Client Contact Code", 
    i."Last Name", 
    i."Animal Code", 
    v."EvPetID",
    i."Animal Name", 
    v."PetID", 
    v."SubscriptionStatus",
    v."ProductCode",
    v."ActualEvWp",
    SUM(i."Total Invoiced (incl)") AS Total_Invoiced_Summary
FROM 
    eV_InvoiceLines i
LEFT JOIN 
    vera_PetCarePlans v
ON 
    i."Animal Code" = v.EvPetID
WHERE 
    i."Type" = 'Item'  -- Only include rows where "Type" is 'Item'
    AND v."SubscriptionStatus" IS NULL  	
    AND i."Product Name" IS Not "Subscription Fee"  -- Only include rows where ActualEvWp is NULL	

GROUP BY 
    i."Invoice #";
