import os
import sys
sys.path.append(os.getcwd())
from tools.data_fetch.yahoo.yahoo import YahooAPI

if __name__ == "__main__":
    tickers = [
        'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'BRK-B', 'TSLA', 'META', 'NVDA', 'TSMC', 'JPM',
        'JNJ', 'V', 'WMT', 'UNH', 'PG', 'MA', 'XOM', 'HD', 'BAC', 'DIS',
        'VZ', 'KO', 'CMCSA', 'CSCO', 'PFE', 'PEP', 'ADBE', 'INTC', 'NFLX', 'ABT',
        'TMO', 'MRK', 'CRM', 'NKE', 'ACN', 'AVGO', 'MCD', 'COST', 'NEE', 'TXN',
        'LLY', 'ORCL', 'PM', 'MDT', 'UPS', 'HON', 'MS', 'UNP', 'IBM', 'QCOM',
        'LIN', 'AMGN', 'CVX', 'BMY', 'SBUX', 'BLK', 'RTX', 'GE', 'AMAT', 'SCHW',
        'INTU', 'NOW', 'T', 'LOW', 'SPGI', 'AXP', 'BA', 'MMM', 'CAT', 'GILD',
        'PLD', 'MDLZ', 'ISRG', 'C', 'ADP', 'DE', 'AMT', 'DUK', 'CI', 'MO',
        'CB', 'MU', 'SO', 'EL', 'BKNG', 'ADI', 'EW', 'ZTS', 'GD', 'SYK',
        'ICE', 'PGR', 'REGN', 'LMT', 'AON', 'WM', 'CSX', 'MMC', 'USB', 'DHR'
    ]
    
    # mapping for ticker symbols that had issues
    ticker_corrections = {
        'TSMC': 'TSM',    
        'BRK.A': 'BRK-B',  
        'META': 'META',    
    }
    
    tickers = [ticker_corrections.get(ticker, ticker) for ticker in tickers]
    
    yahoo_api = YahooAPI()
    yahoo_api.download_and_save(tickers, interval='1d')

    # tickers details :

    # AAPL: Apple Inc. - Manufacturer of electronic devices, software, and digital services (iPhone, Mac, iPad).
    # MSFT: Microsoft Corporation - Developer of software, hardware, and cloud services (Windows, Office, Azure).
    # GOOGL: Alphabet Inc. - Parent company of Google, specializing in online search services, advertising, and technology.
    # AMZN: Amazon.com Inc. - E-commerce giant and provider of cloud services (AWS).
    # BRK.A: Berkshire Hathaway Inc. - Diversified conglomerate with investments across various sectors (insurance, energy, etc.).
    # TSLA: Tesla Inc. - Manufacturer of electric vehicles and renewable energy solutions.
    # META: Meta Platforms Inc. - Parent company of Facebook, specializing in social media and virtual reality.
    # NVDA: NVIDIA Corporation - Designer of graphics processors and technology for artificial intelligence.
    # TSM: Taiwan Semiconductor Manufacturing Company - Leading global manufacturer of semiconductors.
    # JPM: JPMorgan Chase & Co. - Major investment bank and financial services provider.
    # JNJ: Johnson & Johnson - Manufacturer of pharmaceuticals, medical devices, and consumer health products.
    # V: Visa Inc. - Global payments technology company facilitating digital payments.
    # WMT: Walmart Inc. - Multinational retail corporation operating a chain of hypermarkets, discount department stores, and grocery stores.
    # UNH: UnitedHealth Group Incorporated - Provider of healthcare products and insurance services.
    # PG: Procter & Gamble Co. - Producer of consumer goods including health, hygiene, and home products.
    # MA: Mastercard Incorporated - Global payments technology company specializing in digital payment solutions.
    # XOM: Exxon Mobil Corporation - Major oil and gas corporation.
    # HD: Home Depot Inc. - Retailer of home improvement and construction products and services.
    # BAC: Bank of America Corporation - Financial services company offering banking and investment services.
    # DIS: The Walt Disney Company - Global entertainment and media conglomerate.
    # VZ: Verizon Communications Inc. - Telecommunications company providing wireless services and broadband.
    # KO: The Coca-Cola Company - Manufacturer of beverages including soft drinks.
    # CMCSA: Comcast Corporation - Provider of cable television, internet, and telephone services.
    # CSCO: Cisco Systems Inc. - Designer and manufacturer of networking hardware and telecommunications equipment.
    # PFE: Pfizer Inc. - Pharmaceutical company known for developing medications and vaccines.
    # PEP: PepsiCo Inc. - Producer of beverages and snack foods.
    # ADBE: Adobe Inc. - Software company known for creative and multimedia software products.
    # INTC: Intel Corporation - Manufacturer of semiconductor chips and computing devices.
    # NFLX: Netflix Inc. - Streaming service provider of films and television series.
    # ABT: Abbott Laboratories - Global healthcare company specializing in diagnostics, medical devices, and nutrition products.
    # TMO: Thermo Fisher Scientific Inc. - Provider of scientific instrumentation, reagents, and consumables.
    # MRK: Merck & Co., Inc. - Pharmaceutical company focused on health and wellness.
    # CRM: Salesforce.com Inc. - Cloud-based software company specializing in customer relationship management (CRM).
    # NKE: Nike Inc. - Sportswear and equipment manufacturer.
    # ACN: Accenture plc - Global professional services company specializing in consulting and technology services.
    # AVGO: Broadcom Inc. - Designer of semiconductor and infrastructure software solutions.
    # MCD: McDonald's Corporation - Fast food restaurant chain.
    # COST: Costco Wholesale Corporation - Membership-based warehouse club retailer.
    # NEE: NextEra Energy Inc. - Renewable energy company.
    # TXN: Texas Instruments Inc. - Manufacturer of semiconductor and electronics products.
    # LLY: Eli Lilly and Company - Global pharmaceutical company focusing on healthcare solutions.
    # ORCL: Oracle Corporation - Software and hardware company specializing in database management and cloud services.
    # PM: Philip Morris International Inc. - Manufacturer of tobacco products.
    # MDT: Medtronic plc - Global leader in medical technology and services.
    # UPS: United Parcel Service, Inc. - Package delivery and supply chain management company.
    # HON: Honeywell International Inc. - Conglomerate involved in various industries including aerospace, building technologies, and performance materials.
    # MS: Morgan Stanley - Global financial services firm offering investment banking, wealth management, and other services.
    # UNP: Union Pacific Corporation - Railroad company providing freight transportation services.
    # IBM: International Business Machines Corporation - Technology and consulting company.
    # QCOM: Qualcomm Incorporated - Developer of semiconductor and telecommunications products.
    # LIN: Linde plc - Global industrial gases and engineering company.
    # AMGN: Amgen Inc. - Biotechnology company focused on novel therapies.
    # CVX: Chevron Corporation - Multinational energy corporation involved in oil, gas, and geothermal energy.
    # BMY: Bristol-Myers Squibb Company - Biopharmaceutical company known for innovative medicines.
    # SBUX: Starbucks Corporation - Coffeehouse chain known for its specialty coffee and beverages.
    # BLK: BlackRock, Inc. - Global asset management firm.
    # RTX: Raytheon Technologies Corporation - Aerospace and defense company.
    # GE: General Electric Company - Multinational conglomerate focusing on various industries including aviation, healthcare, and power.
    # AMAT: Applied Materials, Inc. - Supplier of equipment, services, and software for semiconductor manufacturing.
    # SCHW: Charles Schwab Corporation - Financial services company providing investment and brokerage services.
    # INTU: Intuit Inc. - Financial software company known for products like TurboTax and QuickBooks.
    # NOW: ServiceNow, Inc. - Provider of cloud-based services for digital workflows.
    # T: AT&T Inc. - Telecommunications company providing wireless, broadband, and media services.
    # LOW: Lowe’s Companies, Inc. - Retailer specializing in home improvement products and services.
    # SPGI: S&P Global Inc. - Provider of financial market intelligence and analytics.
    # AXP: American Express Company - Financial services corporation known for its charge cards and travel services.
    # BA: The Boeing Company - Aerospace company that designs and manufactures airplanes, satellites, and defense systems.
    # MMM: 3M Company - Conglomerate involved in manufacturing and innovation across various sectors including healthcare and consumer goods.
    # CAT: Caterpillar Inc. - Manufacturer of construction and mining equipment.
    # GILD: Gilead Sciences, Inc. - Biopharmaceutical company focusing on antiviral drugs.
    # PLD: Prologis, Inc. - Real estate investment trust focusing on logistics and industrial properties.
    # MDLZ: Mondelēz International, Inc. - Snack food and beverage company.
    # ISRG: Intuitive Surgical, Inc. - Developer of robotic-assisted surgical systems.
    # C: Citigroup Inc. - Multinational banking and financial services corporation.
    # ADP: Automatic Data Processing, Inc. - Provider of human resources management software and services.
    # DE: Deere & Company - Manufacturer of agricultural, construction, and forestry machinery.
    # AMT: American Tower Corporation - Owner and operator of wireless and broadcast communications infrastructure.
    # DUK: Duke Energy Corporation - Energy company providing electricity and natural gas.
    # CI: Cigna Corporation - Global health service company providing insurance and healthcare services.
    # MO: Altria Group, Inc. - Tobacco company known for its cigarette brands.
    # CB: Chubb Limited - Global insurance company offering property and casualty insurance.
    # MU: Micron Technology, Inc. - Manufacturer of memory and storage solutions.
    # SO: Southern Company - Energy company providing electricity and natural gas.
    # EL: Estée Lauder Companies Inc. - Manufacturer and marketer of skincare, makeup, and fragrance products.
    # BKNG: Booking Holdings Inc. - Provider of online travel and related services.
    # ADI: Analog Devices, Inc. - Designer of analog, mixed-signal, and digital signal processing integrated circuits.
    # EW: Edwards Lifesciences Corporation - Provider of heart valve therapies and hemodynamic monitoring.
    # ZTS: Zoetis Inc. - Animal health company.
    # GD : General Dynamics Corporation - Aerospace and defense company.
    # SYK: Stryker Corporation - Medical technology company specializing in orthopedic and surgical products.
    # ICE: Intercontinental Exchange, Inc. - Operator of global exchanges and clearing houses.
    # PGR: Progressive Corporation - Insurance company providing auto, home, and other types of insurance.
    # REGN: Regeneron Pharmaceuticals, Inc. - Biopharmaceutical company focused on developing therapies for serious medical conditions.
    # LMT: Lockheed Martin Corporation - Aerospace, defense, and security company.
    # AON: Aon plc - Global professional services firm providing risk, retirement, and health solutions.
    # WM: Waste Management, Inc. - Provider of waste management and environmental services.
    # CSX: CSX Corporation - Provider of rail-based transportation services.
    # MMC: Marsh & McLennan Companies, Inc. - Professional services firm specializing in insurance brokerage and risk management.
    # USB: U.S. Bancorp - Financial services holding company for U.S. Bank.
    # DHR: Danaher Corporation - Global science and technology innovator focusing on diagnostics, life sciences, and environmental solutions.