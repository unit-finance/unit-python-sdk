from unit.utils import date_utils
from unit.models import *
from typing import IO

ApplicationStatus = Literal["Approved", "Denied", "Pending", "PendingReview", "AwaitingDocuments", "Canceled"]

DocumentType = Literal["IdDocument", "Passport", "AddressVerification", "CertificateOfIncorporation",
                       "EmployerIdentificationNumberConfirmation"]

ReasonCode = Literal["PoorQuality", "NameMismatch", "SSNMismatch", "AddressMismatch", "DOBMismatch", "ExpiredId",
                     "EINMismatch", "StateMismatch", "Other"]

ApplicationTypes = Literal["individualApplication", "businessApplication"]


Industry = Literal["Retail", "Wholesale", "Restaurants", "Hospitals", "Construction", "Insurance", "Unions",
                   "RealEstate", "FreelanceProfessional", "OtherProfessionalServices", "OnlineRetailer",
                   "OtherEducationServices"]

AnnualRevenue = Literal['UpTo250k', 'Between250kAnd500k', 'Between500kAnd1m', 'Between1mAnd5m', 'Over5m', 'UpTo50k',
                        'Between50kAnd100k', 'Between100kAnd200k', 'Between200kAnd500k', 'Over500k']

NumberOfEmployees = Literal['One', 'Between2And5', 'Between5And10', 'Over10', 'UpTo10', 'Between10And50',
                            'Between50And100', 'Between100And500', 'Over500']

CashFlow = Literal['Unpredictable', 'Predictable']

BusinessVertical = Literal['AdultEntertainmentDatingOrEscortServices', 'AgricultureForestryFishingOrHunting',
                           'ArtsEntertainmentAndRecreation', 'BusinessSupportOrBuildingServices', 'Cannabis',
                           'Construction', 'DirectMarketingOrTelemarketing', 'EducationalServices',
                           'FinancialServicesCryptocurrency', 'FinancialServicesDebitCollectionOrConsolidation',
                           'FinancialServicesMoneyServicesBusinessOrCurrencyExchange', 'FinancialServicesOther',
                           'FinancialServicesPaydayLending', 'GamingOrGambling', 'HealthCareAndSocialAssistance',
                           'HospitalityAccommodationOrFoodServices', 'LegalAccountingConsultingOrComputerProgramming',
                           'Manufacturing', 'Mining', 'Nutraceuticals', 'PersonalCareServices', 'PublicAdministration',
                           'RealEstate', 'ReligiousCivicAndSocialOrganizations', 'RepairAndMaintenance', 'RetailTrade',
                           'TechnologyMediaOrTelecom', 'TransportationOrWarehousing', 'Utilities', 'WholesaleTrade']

Revocability = Literal['Revocable', 'Irrevocable']
SourceOfFunds = Literal['Inheritance', 'Salary', 'Savings', 'InvestmentReturns', 'Gifts']

# Types for Thread Applications (v2)

# Individual types
ThreadApplicationIndividualAccountPurpose = Literal[
    'PayrollOrDirectDeposit', 'PersonalSavingsOrEmergencyFund', 'EverydaySpending', 'DomesticP2PAndBillPay',
    'InternationalRemittances', 'CashHeavyPersonalIncome', 'PropertyPurchaseOrInvestment',
    'EducationOrStudentUse', 'TrustOrEstateDistributions', 'Cryptocurrency'
]

ThreadApplicationIndividualSourceOfFunds = Literal[
    'SalaryOrWages', 'BusinessIncome', 'InvestmentIncome', 'RetirementSavings', 'Inheritance',
    'Gift', 'SaleOfAssets', 'LegalSettlement', 'LoanProceeds'
]

ThreadApplicationIndividualTransactionVolume = Literal[
    'LessThan1K', 'Between1KAnd5K', 'Between5KAnd15K', 'Between15KAnd30K', 'Between30KAnd60K', 'GreaterThan60K'
]

# Business types
ThreadApplicationBusinessAccountPurpose = Literal[
    'RetailSalesInPerson', 'EcommerceSales', 'CashHeavyIncomeAndOperations', 'ImportExportTradeOperations',
    'ProfessionalServicesNotHandlingFunds', 'ProfessionalServicesHandlingFunds',
    'HoldingOrInvestmentCompanyOperations', 'PropertyManagementOrRealEstateOperations',
    'CharitableOrNonProfitOrganizationOperations', 'ConstructionAndContractingOperations',
    'CommercialCashOperations', 'FreightForwardingOrLogisticsOperations', 'ThirdPartyPaymentProcessing',
    'TechnologyStartupOperations', 'WholesaleDistributionOperations', 'FranchiseOperationOperations',
    'HealthcareProviderOperations', 'EducationalInstitutionOperations'
]

ThreadApplicationBusinessSourceOfFunds = Literal[
    'SalesOfGoods', 'SalesOfServices', 'CustomerPayments', 'InvestmentCapital', 'BusinessLoans',
    'OwnerContributions', 'FranchiseRevenue', 'RentalIncome', 'GovernmentContractsOrGrants',
    'DonationsOrFundraising', 'MembershipFeesOrSubscriptions', 'LicensingOrRoyalties',
    'CommissionIncome', 'ImportExportRevenue', 'CryptocurrencyRelatedActivity'
]

ThreadApplicationBusinessTransactionVolume = Literal[
    'LessThan10K', 'Between10KAnd50K', 'Between50KAnd250K', 'Between250KAnd1M', 'Between1MAnd2M', 'GreaterThan2M'
]

ThreadApplicationSoleProprietorTransactionVolume = Literal[
    'LessThan5K', 'Between5KAnd20K', 'Between20KAnd75K', 'Between75KAnd150K', 'Between150KAnd300K', 'GreaterThan300K'
]

ThreadApplicationBusinessIndustry = Literal[
    # Retail
    'GroceryStoresOrSupermarkets', 'ConvenienceStores', 'SpecialtyFoodRetailers', 'GasStationsWithRetail',
    'GeneralMerchandiseOrDepartmentStores', 'OnlineRetailOrECommerce', 'SubscriptionAndMembershipPlatforms',
    'DirectToConsumerBrands', 'Cannabis',
    # Financial Services
    'BanksOrCreditUnions', 'FinTechOrPaymentProcessing', 'InsuranceProviders', 'InvestmentAdvisorsOrBrokerDealers',
    'LendingOrMortgageCompanies', 'TreasuryManagementPlatforms', 'PersonalFinanceAppsOrAIAssistants',
    'RetirementPlanning', 'RealEstateInvestmentPlatforms', 'MoneyServiceBusinesses', 'Cryptocurrency',
    'DebtCollection', 'PaydayLending', 'Gambling',
    # Food & Agriculture
    'FarmsOrAgriculturalProducers', 'FoodWholesalersOrDistributors', 'RestaurantsOrCafes', 'BarsOrNightclubs',
    'CateringServices', 'FarmersMarkets', 'RestaurantTechAndPOSProviders',
    # Healthcare
    'HospitalsOrClinics', 'Pharmacies', 'MedicalEquipmentSuppliers', 'BiotechnologyFirms', 'HomeHealthServices',
    'HealthcareStaffingPlatforms', 'WellnessAndBenefitsPlatforms', 'HealthcareAndSocialAssistance',
    # Professional Services
    'LegalServices', 'AccountingOrAuditingFirms', 'ConsultingFirms', 'MarketingOrAdvertisingAgencies',
    'RealEstateAgentsOrPropertyManagers', 'CorporateServicesAndIncorporation', 'HRAndWorkforceManagementPlatforms',
    'DirectMarketingOrTelemarketing', 'LegalAccountingConsultingOrComputerProgramming',
    # Manufacturing
    'ChemicalManufacturing', 'ElectronicsOrHardwareManufacturing', 'AutomotiveManufacturing',
    'ConstructionMaterials', 'TextilesOrApparel', 'Mining',
    # Real Estate & Construction
    'RealEstate', 'Construction',
    # Other
    'TransportationOrWarehousing', 'WholesaleTrade', 'BusinessSupportOrBuildingServices',
    'EscortServices', 'DatingOrAdultEntertainment'
]

ThreadApplicationEntityType = Literal[
    'Estate', 'Trust', 'ForeignFinancialInstitution', 'DomesticFinancialInstitution', 'GovernmentEntityOrAgency',
    'ReligiousOrganization', 'Charity', 'LLC', 'Partnership', 'PubliclyTradedCorporation',
    'PrivatelyHeldCorporation', 'NotForProfitOrganization'
]

ThreadApplicationUSNexus = Literal[
    'Employees', 'Customers', 'PhysicalOfficeOrFacility', 'BankingRelationships', 'NotAvailable'
]

ThreadApplicationProfession = Literal[
    'Accountant', 'Actor', 'Administrator', 'Analyst', 'Architect', 'Artist', 'Attorney', 'Auditor',
    'Banker', 'Barber', 'Bartender', 'Bookkeeper', 'Broker', 'BusinessOwner', 'Chef', 'Clergy', 'Coach',
    'Consultant', 'Contractor', 'CustomerServiceRepresentative', 'Dentist', 'Designer', 'Developer',
    'Doctor', 'Driver', 'Economist', 'Educator', 'Electrician', 'Engineer', 'Entrepreneur', 'EventPlanner',
    'Executive', 'Farmer', 'FinancialAdvisor', 'Firefighter', 'Fisherman', 'FlightAttendant', 'Freelancer',
    'GovernmentEmployee', 'GraphicDesigner', 'HealthcareWorker', 'HRProfessional', 'InsuranceAgent',
    'Investor', 'ITSpecialist', 'Janitor', 'Journalist', 'Laborer', 'LawEnforcementOfficer', 'Lawyer',
    'Librarian', 'LogisticsCoordinator', 'Manager', 'MarketingProfessional', 'Mechanic', 'MilitaryPersonnel',
    'Musician', 'Nurse', 'Optometrist', 'Painter', 'Pharmacist', 'Photographer', 'PhysicalTherapist',
    'Pilot', 'Plumber', 'PoliceOfficer', 'Professor', 'Programmer', 'ProjectManager', 'RealEstateAgent',
    'Receptionist', 'Researcher', 'RetailWorker', 'Salesperson', 'Scientist', 'SocialWorker',
    'SoftwareEngineer', 'Student', 'Surgeon', 'Teacher', 'Technician', 'Therapist', 'Trainer',
    'Veterinarian', 'WaiterWaitress', 'Writer'
]


class BaseApplication(UnitDTO):
    def __init__(self, _id: str, _type: str, created_at: datetime, status: ApplicationStatus, message: str,
                 archived: bool, relationships: Dict[str, Relationship], updated_at: Optional[datetime],
                 tags: Optional[object]):
        self.id = _id
        self.type = _type
        self.attributes = {"createdAt": created_at, "status": status, "message": message,  "archived": archived,
                           "updatedAt": updated_at, "tags": tags}
        self.relationships = relationships


class IndividualApplicationDTO(BaseApplication):
    def __init__(self, id: str, created_at: datetime, full_name: FullName, address: Address, date_of_birth: date,
                 email: str, phone: Phone, status: ApplicationStatus, ssn: Optional[str], message: str,
                 ip: Optional[str], ein: Optional[str], dba: Optional[str],
                 sole_proprietorship: Optional[bool], tags: Optional[Dict[str, str]],
                 relationships: Optional[Dict[str, Relationship]], archived: Optional[bool],
                 power_of_attorney_agent: Optional[Agent], id_theft_score: Optional[int], industry: Optional[Industry],
                 passport: Optional[str], nationality: Optional[str], updated_at: Optional[datetime]):
        super().__init__(id, "individualApplication", created_at, status, message, archived, relationships, updated_at,
                         tags)
        self.attributes.update({"fullName": full_name, "address": address, "dateOfBirth": date_of_birth,
                                "email": email, "phone": phone, "ssn": ssn, "ip": ip, "ein": ein, "dba": dba,
                                "powerOfAttorneyAgent": power_of_attorney_agent,
                                "soleProprietorship": sole_proprietorship, "industry": industry, "passport": passport,
                                "nationality": nationality,  "idTheftScore": id_theft_score})

    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return IndividualApplicationDTO(
            _id, date_utils.to_datetime(attributes["createdAt"]),
            FullName.from_json_api(attributes["fullName"]), Address.from_json_api(attributes["address"]),
            date_utils.to_date(attributes["dateOfBirth"]),
            attributes["email"], Phone.from_json_api(attributes["phone"]), attributes["status"],
            attributes.get("ssn"), attributes.get("message"), attributes.get("ip"),
            attributes.get("ein"), attributes.get("dba"), attributes.get("soleProprietorship"),
            attributes.get("tags"), relationships, attributes.get("archived"),
            Agent.from_json_api(attributes.get("powerOfAttorneyAgent")), attributes.get("idTheftScore"),
            attributes.get("industry"), attributes.get("passport"), attributes.get("nationality"),
            date_utils.to_datetime(attributes.get("updatedAt")))


class IndividualThreadApplicationDTO(BaseApplication):
    def __init__(self, id: str, status: ApplicationStatus, message: str, created_at: datetime,
                 updated_at: Optional[datetime], ssn: Optional[str], passport: Optional[str],
                 nationality: Optional[str], full_name: FullName, date_of_birth: date, address: Address,
                 phone: Phone, email: str, ip: Optional[str], sole_proprietorship: Optional[bool],
                 ein: Optional[str], dba: Optional[str], archived: Optional[bool],
                 id_theft_score: Optional[int], tags: Optional[Dict[str, str]],
                 account_purpose: Optional[ThreadApplicationIndividualAccountPurpose],
                 account_purpose_description: Optional[str],
                 source_of_funds: Optional[ThreadApplicationIndividualSourceOfFunds],
                 transaction_volume: Optional[ThreadApplicationIndividualTransactionVolume],
                 profession: Optional[ThreadApplicationProfession],
                 relationships: Optional[Dict[str, Relationship]]):
        super().__init__(id, "individualApplication", created_at, status, message, archived, relationships, updated_at,
                         tags)
        self.attributes.update({"ssn": ssn, "passport": passport, "nationality": nationality,
                                "fullName": full_name, "dateOfBirth": date_of_birth, "address": address,
                                "phone": phone, "email": email, "ip": ip,
                                "soleProprietorship": sole_proprietorship, "ein": ein, "dba": dba,
                                "idTheftScore": id_theft_score,
                                "accountPurpose": account_purpose,
                                "accountPurposeDescription": account_purpose_description,
                                "sourceOfFunds": source_of_funds,
                                "transactionVolume": transaction_volume,
                                "profession": profession})

    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return IndividualThreadApplicationDTO(
            _id, attributes["status"], attributes.get("message"),
            date_utils.to_datetime(attributes["createdAt"]),
            date_utils.to_datetime(attributes.get("updatedAt")),
            attributes.get("ssn"), attributes.get("passport"), attributes.get("nationality"),
            FullName.from_json_api(attributes["fullName"]), date_utils.to_date(attributes["dateOfBirth"]),
            Address.from_json_api(attributes["address"]), Phone.from_json_api(attributes["phone"]),
            attributes["email"], attributes.get("ip"),
            attributes.get("soleProprietorship"), attributes.get("ein"), attributes.get("dba"),
            attributes.get("archived"), attributes.get("idTheftScore"), attributes.get("tags"),
            attributes.get("accountPurpose"), attributes.get("accountPurposeDescription"),
            attributes.get("sourceOfFunds"), attributes.get("transactionVolume"),
            attributes.get("profession"),
            relationships)


class BusinessApplicationDTO(BaseApplication):
    def __init__(self, id: str, created_at: datetime, name: str, address: Address, phone: Phone,
                 status: ApplicationStatus, state_of_incorporation: str, entity_type: EntityType,
                 contact: BusinessContact, officer: Officer, beneficial_owners: [BeneficialOwner],
                 message: Optional[str], ein: Optional[str], dba: Optional[str], tags: Optional[Dict[str, str]],
                 relationships: Optional[Dict[str, Relationship]], updated_at: Optional[datetime],
                 industry: Optional[Industry], archived: Optional[bool]):
        super().__init__(id, "businessApplication", created_at, status, message, archived, relationships, updated_at,
                         tags)
        self.attributes.update({"name": name, "address": address, "phone": phone,
                                "stateOfIncorporation": state_of_incorporation, "message": message, "ein": ein,
                                "entityType": entity_type, "dba": dba, "contact": contact, "officer": officer,
                                "beneficialOwners": beneficial_owners, "industry": industry})

    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return BusinessApplicationDTO(
            _id, date_utils.to_datetime(attributes["createdAt"]), attributes.get("name"),
            Address.from_json_api(attributes["address"]), Phone.from_json_api(attributes["phone"]),
            attributes["status"], attributes.get("stateOfIncorporation"), attributes.get("entityType"),
            BusinessContact.from_json_api(attributes["contact"]), Officer.from_json_api(attributes["officer"]),
            BeneficialOwner.from_json_api(attributes["beneficialOwners"]), attributes.get("message"),
            attributes.get("ein"), attributes.get("dba"), attributes.get("tags"), relationships,
            date_utils.to_datetime(attributes.get("updatedAt")), attributes.get("industry"), attributes.get("archived")
        )


class BusinessThreadApplicationDTO(BaseApplication):
    def __init__(self, id: str, status: ApplicationStatus, message: str, created_at: datetime,
                 updated_at: Optional[datetime], name: str, dba: Optional[str], address: Address,
                 operating_address: Optional[Address], phone: Phone, state_of_incorporation: str,
                 ein: str, website: Optional[str], contact: BusinessContact, officer: Officer,
                 beneficial_owners: List[BeneficialOwner], ip: Optional[str], archived: Optional[bool],
                 tags: Optional[Dict[str, str]],
                 source_of_funds: Optional[ThreadApplicationBusinessSourceOfFunds],
                 source_of_funds_description: Optional[str],
                 business_industry: Optional[ThreadApplicationBusinessIndustry],
                 business_description: Optional[str],
                 is_regulated: Optional[bool], regulator_name: Optional[str],
                 us_nexus: Optional[List[ThreadApplicationUSNexus]],
                 account_purpose: Optional[ThreadApplicationBusinessAccountPurpose],
                 account_purpose_description: Optional[str],
                 transaction_volume: Optional[ThreadApplicationBusinessTransactionVolume],
                 stock_exchange_name: Optional[str], stock_symbol: Optional[str],
                 countries_of_operation: Optional[List[str]], year_of_incorporation: Optional[str],
                 entity_type: ThreadApplicationEntityType,
                 relationships: Optional[Dict[str, Relationship]]):
        super().__init__(id, "businessApplication", created_at, status, message, archived, relationships, updated_at,
                         tags)
        self.attributes.update({"name": name, "dba": dba, "address": address,
                                "operatingAddress": operating_address, "phone": phone,
                                "stateOfIncorporation": state_of_incorporation, "ein": ein,
                                "website": website, "contact": contact, "officer": officer,
                                "beneficialOwners": beneficial_owners, "ip": ip,
                                "sourceOfFunds": source_of_funds,
                                "sourceOfFundsDescription": source_of_funds_description,
                                "businessIndustry": business_industry,
                                "businessDescription": business_description,
                                "isRegulated": is_regulated, "regulatorName": regulator_name,
                                "usNexus": us_nexus,
                                "accountPurpose": account_purpose,
                                "accountPurposeDescription": account_purpose_description,
                                "transactionVolume": transaction_volume,
                                "stockExchangeName": stock_exchange_name, "stockSymbol": stock_symbol,
                                "countriesOfOperation": countries_of_operation,
                                "yearOfIncorporation": year_of_incorporation,
                                "entityType": entity_type})

    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        operating_address = Address.from_json_api(attributes.get("operatingAddress")) if attributes.get("operatingAddress") else None
        return BusinessThreadApplicationDTO(
            _id, attributes["status"], attributes.get("message"),
            date_utils.to_datetime(attributes["createdAt"]),
            date_utils.to_datetime(attributes.get("updatedAt")),
            attributes.get("name"), attributes.get("dba"),
            Address.from_json_api(attributes["address"]), operating_address,
            Phone.from_json_api(attributes["phone"]),
            attributes.get("stateOfIncorporation"), attributes.get("ein"), attributes.get("website"),
            BusinessContact.from_json_api(attributes["contact"]), Officer.from_json_api(attributes["officer"]),
            BeneficialOwner.from_json_api(attributes.get("beneficialOwners")),
            attributes.get("ip"), attributes.get("archived"), attributes.get("tags"),
            attributes.get("sourceOfFunds"), attributes.get("sourceOfFundsDescription"),
            attributes.get("businessIndustry"), attributes.get("businessDescription"),
            attributes.get("isRegulated"), attributes.get("regulatorName"),
            attributes.get("usNexus"),
            attributes.get("accountPurpose"), attributes.get("accountPurposeDescription"),
            attributes.get("transactionVolume"),
            attributes.get("stockExchangeName"), attributes.get("stockSymbol"),
            attributes.get("countriesOfOperation"), attributes.get("yearOfIncorporation"),
            attributes.get("entityType"),
            relationships)


ApplicationDTO = Union[IndividualApplicationDTO, BusinessApplicationDTO]

ThreadApplicationDTO = Union[IndividualThreadApplicationDTO, BusinessThreadApplicationDTO]


class BaseCreateIndividualApplicationRequest(UnitRequest):
    def __init__(self, full_name: FullName, date_of_birth: date, address: Address, email: str, phone: Phone,
                 ip: Optional[str] = None, ein: Optional[str] = None, dba: Optional[str] = None,
                 sole_proprietorship: Optional[bool] = None, passport: Optional[str] = None,
                 nationality: Optional[str] = None, ssn: Optional[str] = None,
                 device_fingerprints: Optional[List[DeviceFingerprint]] = None, idempotency_key: str = None,
                 tags: Optional[Dict[str, str]] = None, jwt_subject: Optional[str] = None,
                 power_of_attorney_agent: Optional[Agent] = None, evaluation_params: Optional[EvaluationParams] = None,
                 occupation: Optional[Occupation] = None, annual_income: Optional[AnnualIncome] = None,
                 source_of_income: Optional[SourceOfIncome] = None):
        self.full_name = full_name
        self.date_of_birth = date_of_birth
        self.address = address
        self.email = email
        self.phone = phone
        self.ip = ip
        self.ein = ein
        self.dba = dba
        self.sole_proprietorship = sole_proprietorship
        self.ssn = ssn
        self.passport = passport
        self.nationality = nationality
        self.device_fingerprints = device_fingerprints
        self.idempotency_key = idempotency_key
        self.tags = tags
        self.jwt_subject = jwt_subject
        self.power_of_attorney_agent = power_of_attorney_agent
        self.evaluation_params = evaluation_params
        self.occupation = occupation
        self.annual_income = annual_income
        self.source_of_income = source_of_income

    def to_json_api(self) -> Dict:
        return super().to_payload("individualApplication")

    def __repr__(self):
        return json.dumps(self.to_json_api())


class CreateIndividualApplicationRequest(BaseCreateIndividualApplicationRequest):
    pass


class CreateIndividualThreadApplicationRequest(UnitRequest):
    def __init__(self, ssn: Optional[str], passport: Optional[str], nationality: Optional[str],
                 full_name: FullName, date_of_birth: date, address: Address, phone: Phone, email: str,
                 evaluation_params: Optional[EvaluationParams] = None, ip: Optional[str] = None,
                 tags: Optional[Dict[str, str]] = None, idempotency_key: Optional[str] = None,
                 device_fingerprints: Optional[List[DeviceFingerprint]] = None,
                 jwt_subject: Optional[str] = None, banks: Optional[List[str]] = None,
                 account_purpose: Optional[ThreadApplicationIndividualAccountPurpose] = None,
                 account_purpose_description: Optional[str] = None,
                 source_of_funds: Optional[ThreadApplicationIndividualSourceOfFunds] = None,
                 transaction_volume: Optional[ThreadApplicationIndividualTransactionVolume] = None,
                 transaction_volume_description: Optional[str] = None,
                 profession: Optional[ThreadApplicationProfession] = None):
        self.ssn = ssn
        self.passport = passport
        self.nationality = nationality
        self.full_name = full_name
        self.date_of_birth = date_of_birth
        self.address = address
        self.phone = phone
        self.email = email
        self.evaluation_params = evaluation_params
        self.ip = ip
        self.tags = tags
        self.idempotency_key = idempotency_key
        self.device_fingerprints = device_fingerprints
        self.jwt_subject = jwt_subject
        self.banks = banks
        self.account_purpose = account_purpose
        self.account_purpose_description = account_purpose_description
        self.source_of_funds = source_of_funds
        self.transaction_volume = transaction_volume
        self.transaction_volume_description = transaction_volume_description
        self.profession = profession

    def to_json_api(self) -> Dict:
        return super().to_payload("individualApplication")

    def __repr__(self):
        return json.dumps(self.to_json_api())


class CreateSoleProprietorThreadApplicationRequest(UnitRequest):
    def __init__(self, ssn: Optional[str], passport: Optional[str], nationality: Optional[str],
                 full_name: FullName, date_of_birth: date, address: Address, phone: Phone, email: str,
                 dba: Optional[str] = None, ein: Optional[str] = None, website: Optional[str] = None,
                 evaluation_params: Optional[EvaluationParams] = None, ip: Optional[str] = None,
                 tags: Optional[Dict[str, str]] = None, idempotency_key: Optional[str] = None,
                 device_fingerprints: Optional[List[DeviceFingerprint]] = None,
                 jwt_subject: Optional[str] = None, banks: Optional[List[str]] = None,
                 account_purpose: Optional[ThreadApplicationBusinessAccountPurpose] = None,
                 account_purpose_description: Optional[str] = None,
                 source_of_funds: Optional[ThreadApplicationBusinessSourceOfFunds] = None,
                 transaction_volume: Optional[ThreadApplicationSoleProprietorTransactionVolume] = None,
                 transaction_volume_description: Optional[str] = None,
                 profession: Optional[ThreadApplicationProfession] = None):
        self.ssn = ssn
        self.passport = passport
        self.nationality = nationality
        self.full_name = full_name
        self.date_of_birth = date_of_birth
        self.address = address
        self.phone = phone
        self.email = email
        self.dba = dba
        self.ein = ein
        self.website = website
        self.evaluation_params = evaluation_params
        self.ip = ip
        self.tags = tags
        self.idempotency_key = idempotency_key
        self.device_fingerprints = device_fingerprints
        self.jwt_subject = jwt_subject
        self.banks = banks
        self.account_purpose = account_purpose
        self.account_purpose_description = account_purpose_description
        self.source_of_funds = source_of_funds
        self.transaction_volume = transaction_volume
        self.transaction_volume_description = transaction_volume_description
        self.profession = profession

    def to_json_api(self) -> Dict:
        return super().to_payload("individualApplication")

    def __repr__(self):
        return json.dumps(self.to_json_api())


class CreateBusinessThreadApplicationRequest(UnitRequest):
    def __init__(self, name: str, address: Address, phone: Phone, state_of_incorporation: str, ein: str,
                 entity_type: ThreadApplicationEntityType, contact: BusinessContact, officer: Officer,
                 beneficial_owners: Optional[List[BeneficialOwner]] = None, dba: Optional[str] = None,
                 website: Optional[str] = None, business_description: Optional[str] = None,
                 business_industry: Optional[ThreadApplicationBusinessIndustry] = None,
                 us_nexus: Optional[List[ThreadApplicationUSNexus]] = None,
                 evaluation_params: Optional[EvaluationParams] = None, ip: Optional[str] = None,
                 tags: Optional[Dict[str, str]] = None, idempotency_key: Optional[str] = None,
                 device_fingerprints: Optional[List[DeviceFingerprint]] = None,
                 jwt_subject: Optional[str] = None, banks: Optional[List[str]] = None,
                 account_purpose: Optional[ThreadApplicationBusinessAccountPurpose] = None,
                 account_purpose_description: Optional[str] = None,
                 source_of_funds: Optional[ThreadApplicationBusinessSourceOfFunds] = None,
                 transaction_volume: Optional[ThreadApplicationBusinessTransactionVolume] = None,
                 transaction_volume_description: Optional[str] = None):
        self.name = name
        self.address = address
        self.phone = phone
        self.state_of_incorporation = state_of_incorporation
        self.ein = ein
        self.entity_type = entity_type
        self.contact = contact
        self.officer = officer
        self.beneficial_owners = beneficial_owners if beneficial_owners is not None else []
        self.dba = dba
        self.website = website
        self.business_description = business_description
        self.business_industry = business_industry
        self.us_nexus = us_nexus
        self.evaluation_params = evaluation_params
        self.ip = ip
        self.tags = tags
        self.idempotency_key = idempotency_key
        self.device_fingerprints = device_fingerprints
        self.jwt_subject = jwt_subject
        self.banks = banks
        self.account_purpose = account_purpose
        self.account_purpose_description = account_purpose_description
        self.source_of_funds = source_of_funds
        self.transaction_volume = transaction_volume
        self.transaction_volume_description = transaction_volume_description

    def to_payload(self, payload_type: str) -> Dict:
        payload = super().to_payload(payload_type)
        if self.beneficial_owners == []:
            payload['data']['attributes']['beneficialOwners'] = self.beneficial_owners
        return payload

    def to_json_api(self) -> Dict:
        return self.to_payload("businessApplication")

    def __repr__(self):
        return json.dumps(self.to_json_api())


class CreateBusinessApplicationRequest(UnitRequest):
    def __init__(self, name: str, address: Address, phone: Phone, state_of_incorporation: str, ein: str,
                 contact: BusinessContact, officer: Officer,
                 entity_type: EntityType, beneficial_owners: Optional[List[BeneficialOwner]] = None, dba: Optional[str] = None, ip: Optional[str] = None,
                 website: Optional[str] = None, industry: Optional[Industry] = None,
                 annual_revenue: Optional[AnnualRevenue] = None,
                 number_of_employees: Optional[NumberOfEmployees] = None, cash_flow: Optional[CashFlow] = None,
                 year_of_incorporation: Optional[Union[date, str]] = None,
                 countries_of_operation: Optional[List[str]] = None, stock_symbol: Optional[str] = None,
                 business_vertical: Optional[BusinessVertical] = None,
                 device_fingerprints: Optional[List[DeviceFingerprint]] = None,
                 tags: Optional[Dict[str, str]] = None, idempotency_key: Optional[str] = None
                 ):
        self.name = name
        self.address = address
        self.phone = phone
        self.state_of_incorporation = state_of_incorporation
        self.ein = ein
        self.contact = contact
        self.officer = officer
        self.entity_type = entity_type
        self.beneficial_owners = beneficial_owners if beneficial_owners is not None else []
        self.dba = dba
        self.ip = ip
        self.website = website
        self.industry = industry
        self.annual_revenue = annual_revenue
        self.number_of_employees = number_of_employees
        self.cash_flow = cash_flow
        self.year_of_incorporation = date_utils.to_year_str(year_of_incorporation)
        self.countries_of_operation = countries_of_operation
        self.stock_symbol = stock_symbol
        self.business_vertical = business_vertical
        self.device_fingerprints = device_fingerprints
        self.tags = tags
        self.idempotency_key = idempotency_key

    def to_payload(self, payload_type: str) -> Dict:
        payload = super().to_payload(payload_type)
        if self.beneficial_owners == []:
            payload['data']['attributes']['beneficialOwners'] = self.beneficial_owners
        return payload

    def to_json_api(self) -> Dict:
        return self.to_payload("businessApplication")

    def __repr__(self):
        return json.dumps(self.to_json_api())


class CreateSoleProprietorApplicationRequest(BaseCreateIndividualApplicationRequest):
    def __init__(self, full_name: FullName, date_of_birth: date, address: Address, email: str, phone: Phone,
                 ip: Optional[str] = None, ein: Optional[str] = None, dba: Optional[str] = None,
                 sole_proprietorship: Optional[bool] = None, passport: Optional[str] = None,
                 nationality: Optional[str] = None, ssn: Optional[str] = None,
                 device_fingerprints: Optional[List[DeviceFingerprint]] = None, idempotency_key: Optional[str] = None,
                 tags: Optional[Dict[str, str]] = None, jwt_subject: Optional[str] = None,
                 power_of_attorney_agent: Optional[Agent] = None, evaluation_params: Optional[EvaluationParams] = None,
                 occupation: Optional[Occupation] = None, annual_income: Optional[AnnualIncome] = None,
                 source_of_income: Optional[SourceOfIncome] = None, annual_revenue: Optional[AnnualRevenue] = None,
                 number_of_employees: Optional[NumberOfEmployees] = None,
                 business_vertical: Optional[BusinessVertical] = None):
        super().__init__(full_name, date_of_birth, address, email, phone, ip, ein, dba, sole_proprietorship, passport,
                         nationality, ssn, device_fingerprints, idempotency_key, tags, jwt_subject,
                         power_of_attorney_agent, evaluation_params, occupation, annual_income, source_of_income)
        self.annual_revenue = annual_revenue
        self.number_of_employees = number_of_employees
        self.business_vertical = business_vertical


CreateApplicationRequest = Union[CreateIndividualApplicationRequest, CreateBusinessApplicationRequest,
                                 CreateSoleProprietorApplicationRequest]

CreateThreadApplicationRequest = Union[CreateIndividualThreadApplicationRequest, CreateBusinessThreadApplicationRequest,
                                       CreateSoleProprietorThreadApplicationRequest]


class ApplicationDocumentDTO(object):
    def __init__(self, id: str, status: ApplicationStatus, document_type: DocumentType, description: str,
                 name: Optional[str], address: Optional[Address], date_of_birth: Optional[date],
                 passport: Optional[str], ein: Optional[str], reason_code: Optional[ReasonCode], reason: Optional[str]):
        self.id = id
        self.type = "document"
        self.attributes = {"status": status, "documentType": document_type, "description": description, "name": name,
                           "address": address, "dateOfBirth": date_of_birth, "passport": passport, "ein": ein,
                           "reasonCode": reason_code, "reason": reason}

    @staticmethod
    def from_json_api(_id, _type, attributes):
        address = Address.from_json_api(attributes.get("address")) if attributes.get("address") else None
        return ApplicationDocumentDTO(
            _id, attributes["status"], attributes["documentType"], attributes["description"], attributes.get("name"),
            address, attributes.get("dateOfBirth"), attributes.get("passport"),
            attributes.get("ein"), attributes.get("reasonCode"), attributes.get("reason")
        )


FileType = Literal["jpeg", "png", "pdf"]


class UploadDocumentRequest(object):
    def __init__(self, application_id: str, document_id: str, file: IO, file_type: FileType,
                 is_back_side: Optional[bool] = False):
        self.application_id = application_id
        self.document_id = document_id
        self.file = file
        self.file_type = file_type
        self.is_back_side = is_back_side


class ListApplicationParams(UnitParams):
    def __init__(self, offset: int = 0, limit: int = 100, email: Optional[str] = None,
                 tags: Optional[Dict[str, str]] = None, query: Optional[str] = None,
                 sort: Optional[Literal["createdAt", "-createdAt"]] = None):
        self.offset = offset
        self.limit = limit
        self.email = email
        self.query = query
        self.sort = sort
        self.tags = tags

    def to_dict(self) -> Dict:
        parameters = {"page[limit]": self.limit, "page[offset]": self.offset}
        if self.email:
            parameters["filter[email]"] = self.email
        if self.query:
            parameters["filter[query]"] = self.query
        if self.tags:
            parameters["filter[tags]"] = json.dumps(self.tags)
        if self.sort:
            parameters["sort"] = self.sort
        return parameters


class PatchApplicationRequest(UnitRequest):
    def __init__(self, application_id: str, type: ApplicationTypes = "individualApplication",
                 tags: Optional[Dict[str, str]] = None):
        self.application_id = application_id
        self.type = type
        self.tags = tags

    def to_json_api(self) -> Dict:
        return super().to_payload(self.type, ignore=['application_id', 'type'])


class PatchIndividualApplicationRequest(PatchApplicationRequest):
    def __init__(self, application_id: str, occupation: Optional[Occupation] = None,
                 annual_income: Optional[AnnualIncome] = None, source_of_income: Optional[SourceOfIncome] = None,
                 tags: Optional[Dict[str, str]] = None):
        super().__init__(application_id, tags=tags)
        self.occupation = occupation
        self.annual_income = annual_income
        self.source_of_income = source_of_income


class PatchSoleProprietorApplicationRequest(PatchApplicationRequest):
    def __init__(self, application_id: str, annual_revenue: Optional[AnnualRevenue] = None,
                 number_of_employees: Optional[NumberOfEmployees] = None,
                 business_vertical: Optional[BusinessVertical] = None, website: Optional[str] = None,
                 tags: Optional[Dict[str, str]] = None):
        super().__init__(application_id, tags=tags)
        self.annual_revenue = annual_revenue
        self.number_of_employees = number_of_employees
        self.business_vertical = business_vertical
        self.website = website


class UpdateBusinessAttributes(object):
    def __init__(self, occupation: Optional[Occupation] = None, annual_income: Optional[AnnualIncome] = None,
                 source_of_income: Optional[SourceOfIncome] = None):
        self.occupation = occupation
        self.annual_income = annual_income
        self.source_of_income = source_of_income


class PatchBusinessBeneficialOwnerRequest(UnitRequest):
    def __init__(self, beneficial_owner_id: str, application_id: str, occupation: Optional[Occupation] = None,
                 annual_income: Optional[AnnualIncome] = None, source_of_income: Optional[SourceOfIncome] = None):
        self.beneficial_owner_id = beneficial_owner_id
        self.application_id = application_id
        self.type = "beneficialOwner"
        self.occupation = occupation
        self.annual_income = annual_income
        self.source_of_income = source_of_income

    def to_json_api(self) -> Dict:
        relationships = {"application": Relationship("businessApplication", self.application_id)}
        return super().to_payload(self.type, relationships, ['beneficial_owner_id', 'application_id', 'type'])


class PatchThreadBusinessBeneficialOwnerRequest(UnitRequest):
    def __init__(self, beneficial_owner_id: str, application_id: str, percentage: Optional[int] = None):
        self.beneficial_owner_id = beneficial_owner_id
        self.application_id = application_id
        self.type = "beneficialOwner"
        self.percentage = percentage

    def to_json_api(self) -> Dict:
        relationships = {"application": Relationship("businessApplication", self.application_id)}
        return super().to_payload(self.type, relationships, ['beneficial_owner_id', 'application_id', 'type'])


class PatchBusinessApplicationRequest(PatchApplicationRequest):
    def __init__(self, application_id: str, annual_revenue: Optional[AnnualRevenue] = None,
                 number_of_employees: Optional[NumberOfEmployees] = None, cash_flow: Optional[CashFlow] = None,
                 year_of_incorporation: Optional[str] = None, countries_of_operation: Optional[str] = None,
                 stock_symbol: Optional[str] = None, business_vertical: Optional[BusinessVertical] = None,
                 officer: Optional[UpdateBusinessAttributes] = None, tags: Optional[Dict[str, str]] = None):
        super().__init__(application_id, "businessApplication", tags=tags)
        self.annual_revenue = annual_revenue
        self.number_of_employees = number_of_employees
        self.cash_flow = cash_flow
        self.year_of_incorporation = year_of_incorporation
        self.countries_of_operation = countries_of_operation
        self.stock_symbol = stock_symbol
        self.business_vertical = business_vertical
        self.officer = officer


class PatchIndividualThreadApplicationRequest(PatchApplicationRequest):
    def __init__(self, application_id: str, tags: Optional[Dict[str, str]] = None):
        super().__init__(application_id, "individualApplication", tags=tags)


class PatchSoleProprietorThreadApplicationRequest(PatchApplicationRequest):
    def __init__(self, application_id: str, tags: Optional[Dict[str, str]] = None):
        super().__init__(application_id, "individualApplication", tags=tags)


class PatchBusinessThreadApplicationRequest(PatchApplicationRequest):
    def __init__(self, application_id: str, tags: Optional[Dict[str, str]] = None):
        super().__init__(application_id, "businessApplication", tags=tags)


UnionPatchApplicationRequest = Union[PatchApplicationRequest, PatchIndividualApplicationRequest,
                                     PatchSoleProprietorApplicationRequest, PatchBusinessApplicationRequest]

UnionPatchThreadApplicationRequest = Union[PatchIndividualThreadApplicationRequest,
                                           PatchSoleProprietorThreadApplicationRequest,
                                           PatchBusinessThreadApplicationRequest]


class CancelApplicationRequest(UnitRequest):
    def __init__(self, application_id: str, reason: str):
        self.application_id = application_id
        self.reason = reason

    def to_json_api(self) -> Dict:
        payload = {
            "data": {
                "type": "applicationCancel",
                "attributes": {
                    "reason": self.reason
                }
            }
        }

        return payload

    def __repr__(self):
        return json.dumps(self.to_json_api())

