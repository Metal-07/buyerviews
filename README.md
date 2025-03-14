# BuyerViews

A Django-based product review and recommendation platform that helps users discover and compare products across various categories. The platform integrates with Google Sheets for easy product management and uses Amazon affiliate links.

## Features

- Product browsing by categories
- Product search functionality
- Detailed product information including:
  - Product images
  - Ratings and reviews
  - Pros and cons
  - Direct links to Amazon
- Responsive design using Tailwind CSS
- Google Sheets integration for easy content management

## Tech Stack

- Python 3.x
- Django 5.0.2
- Tailwind CSS
- Google Sheets API
- Font Awesome icons

## Setup

1. Clone the repository:
```bash
git clone https://github.com/Metal-07/buyerviews.git
cd buyerviews
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a .env file in the project root with the following variables:
```
SECRET_KEY=your-secret-key
DB_NAME=buyerviews
DB_USER=postgres
DB_PASSWORD=your-password
DB_HOST=localhost
DB_PORT=5432
SPREADSHEET_ID=your-google-sheets-id
```

5. Set up Google Sheets API:
   - Create a project in Google Cloud Console
   - Enable Google Sheets API
   - Create a service account and download the credentials
   - Save the credentials as `service-account.json` in the project root

6. Run migrations:
```bash
python manage.py migrate
```

7. Import data from Google Sheets:
```bash
python manage.py import_sheet_data
```

8. Run the development server:
```bash
python manage.py runserver
```

Visit http://127.0.0.1:8000/ to see the application.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

[MIT](https://choosealicense.com/licenses/mit/) 