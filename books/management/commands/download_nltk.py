from django.core.management.base import BaseCommand
import nltk

class Command(BaseCommand):
    help = 'Download required NLTK data for text analysis'

    def handle(self, *args, **options):
        self.stdout.write('Downloading NLTK data...')
        
        nltk_downloads = [
            'punkt',
            'punkt_tab', 
            'stopwords',
            'wordnet',
            'averaged_perceptron_tagger'
        ]
        
        for data in nltk_downloads:
            try:
                self.stdout.write(f'Downloading {data}...')
                nltk.download(data, quiet=True)
                self.stdout.write(self.style.SUCCESS(f'✓ {data} downloaded successfully'))
            except Exception as e:
                self.stdout.write(self.style.WARNING(f'⚠ Failed to download {data}: {e}'))
        
        self.stdout.write(self.style.SUCCESS('NLTK data download completed!'))
