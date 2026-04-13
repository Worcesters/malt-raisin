from datetime import timedelta
from decimal import Decimal

from django.core.management.base import BaseCommand
from django.utils import timezone

from apps.catalog.models import AlcoholType, Category, Product
from apps.events.models import Event


class Command(BaseCommand):
    help = "Charge des données de démonstration dans la base."

    def handle(self, *args, **options):
        self.stdout.write("Création des catégories...")
        categories_data = [
            ("Vins Rouges", "vins-rouges", "Les meilleurs vins rouges de France et du monde.", 1),
            ("Vins Blancs", "vins-blancs", "Vins blancs secs, moelleux et liquoreux.", 2),
            ("Bières Artisanales", "bieres-artisanales", "Sélection de bières craft et artisanales.", 3),
            ("Whiskys", "whiskys", "Single malts, blends et whiskys du monde.", 4),
            ("Rhums", "rhums", "Rhums agricoles, vieux et arrangés.", 5),
            ("Champagnes", "champagnes", "Champagnes et crémants d'exception.", 6),
            ("Spiritueux", "spiritueux", "Gin, vodka et autres spiritueux.", 7),
        ]
        categories = {}
        for name, slug, desc, order in categories_data:
            cat, _ = Category.objects.get_or_create(
                slug=slug, defaults={"name": name, "description": desc, "order": order}
            )
            categories[slug] = cat

        self.stdout.write("Création des produits...")
        products_data = [
            ("Château Margaux 2018", "chateau-margaux-2018", categories["vins-rouges"], Decimal("89.90"), AlcoholType.VIN, "75cl", Decimal("13.5"), "Bordeaux, France", True, 15),
            ("Pommard Premier Cru 2019", "pommard-premier-cru-2019", categories["vins-rouges"], Decimal("52.00"), AlcoholType.VIN, "75cl", Decimal("13.0"), "Bourgogne, France", True, 8),
            ("Côtes du Rhône 2021", "cotes-du-rhone-2021", categories["vins-rouges"], Decimal("12.50"), AlcoholType.VIN, "75cl", Decimal("14.0"), "Rhône, France", False, 30),
            ("Chablis Grand Cru 2020", "chablis-grand-cru-2020", categories["vins-blancs"], Decimal("45.00"), AlcoholType.VIN, "75cl", Decimal("12.5"), "Bourgogne, France", True, 12),
            ("Sancerre 2022", "sancerre-2022", categories["vins-blancs"], Decimal("18.90"), AlcoholType.VIN, "75cl", Decimal("12.0"), "Loire, France", False, 25),
            ("Gewurztraminer Vendanges Tardives", "gewurztraminer-vt", categories["vins-blancs"], Decimal("32.00"), AlcoholType.VIN, "75cl", Decimal("13.5"), "Alsace, France", False, 10),
            ("Cuvée Hoppy Days IPA", "cuvee-hoppy-days-ipa", categories["bieres-artisanales"], Decimal("5.90"), AlcoholType.BIERE, "33cl", Decimal("6.5"), "Brasserie artisanale, Paris", True, 48),
            ("Stout Impérial Noir Profond", "stout-imperial-noir", categories["bieres-artisanales"], Decimal("7.50"), AlcoholType.BIERE, "33cl", Decimal("9.0"), "Brasserie du Vieux Lille", False, 36),
            ("Triple Blonde d'Abbaye", "triple-blonde-abbaye", categories["bieres-artisanales"], Decimal("6.20"), AlcoholType.BIERE, "33cl", Decimal("8.5"), "Belgique", False, 40),
            ("Saison Fermière Bio", "saison-fermiere-bio", categories["bieres-artisanales"], Decimal("5.50"), AlcoholType.BIERE, "75cl", Decimal("6.0"), "Normandie, France", False, 24),
            ("Lagavulin 16 ans", "lagavulin-16", categories["whiskys"], Decimal("72.00"), AlcoholType.WHISKY, "70cl", Decimal("43.0"), "Islay, Écosse", True, 10),
            ("Talisker 10 ans", "talisker-10", categories["whiskys"], Decimal("42.00"), AlcoholType.WHISKY, "70cl", Decimal("45.8"), "Skye, Écosse", False, 15),
            ("Nikka From The Barrel", "nikka-from-barrel", categories["whiskys"], Decimal("48.00"), AlcoholType.WHISKY, "50cl", Decimal("51.4"), "Japon", True, 8),
            ("Glenfiddich 18 ans", "glenfiddich-18", categories["whiskys"], Decimal("85.00"), AlcoholType.WHISKY, "70cl", Decimal("40.0"), "Speyside, Écosse", False, 6),
            ("Clément VSOP", "clement-vsop", categories["rhums"], Decimal("38.00"), AlcoholType.RHUM, "70cl", Decimal("40.0"), "Martinique", True, 12),
            ("Diplomatico Reserva Exclusiva", "diplomatico-reserva", categories["rhums"], Decimal("42.00"), AlcoholType.RHUM, "70cl", Decimal("40.0"), "Venezuela", True, 18),
            ("Rhum JM XO", "rhum-jm-xo", categories["rhums"], Decimal("65.00"), AlcoholType.RHUM, "70cl", Decimal("45.0"), "Martinique", False, 5),
            ("Dom Pérignon 2013", "dom-perignon-2013", categories["champagnes"], Decimal("195.00"), AlcoholType.CHAMPAGNE, "75cl", Decimal("12.5"), "Champagne, France", True, 4),
            ("Ruinart Blanc de Blancs", "ruinart-blanc-de-blancs", categories["champagnes"], Decimal("62.00"), AlcoholType.CHAMPAGNE, "75cl", Decimal("12.5"), "Champagne, France", False, 9),
            ("Hendrick's Gin", "hendricks-gin", categories["spiritueux"], Decimal("35.00"), AlcoholType.GIN, "70cl", Decimal("41.4"), "Écosse", False, 20),
            ("Grey Goose Vodka", "grey-goose-vodka", categories["spiritueux"], Decimal("38.00"), AlcoholType.VODKA, "70cl", Decimal("40.0"), "France", False, 15),
        ]

        for name, slug, category, price, atype, volume, degree, origin, featured, stock in products_data:
            Product.objects.get_or_create(
                slug=slug,
                defaults={
                    "name": name,
                    "category": category,
                    "price": price,
                    "alcohol_type": atype,
                    "volume": volume,
                    "alcohol_degree": degree,
                    "origin": origin,
                    "is_featured": featured,
                    "stock": stock,
                    "description": f"Découvrez {name}, un {atype.label.lower()} d'exception en provenance de {origin}. "
                    f"Volume : {volume}, {degree}% vol.",
                },
            )

        self.stdout.write("Création des événements...")
        events_data = [
            (
                "Soirée Dégustation Grands Crus",
                "soiree-degustation-grands-crus",
                "Venez découvrir une sélection exceptionnelle de grands crus bordelais lors de notre soirée dégustation mensuelle. "
                "Au programme : 6 vins d'exception, accompagnés de fromages affinés et de charcuterie artisanale.",
                timezone.now() + timedelta(days=14),
                "Malt & Raisin — 12 rue des Vignerons, Paris",
                True,
            ),
            (
                "Masterclass Whisky Écossais",
                "masterclass-whisky-ecossais",
                "Plongez dans l'univers fascinant des single malts écossais. Notre expert vous guidera à travers les régions "
                "de production et les subtilités de chaque distillerie. Dégustation de 5 whiskys incluse.",
                timezone.now() + timedelta(days=30),
                "Malt & Raisin — 12 rue des Vignerons, Paris",
                True,
            ),
            (
                "Festival des Bières Artisanales",
                "festival-bieres-artisanales",
                "Pour la 3ème édition de notre festival, rencontrez 10 brasseurs artisanaux et dégustez plus de 30 bières "
                "craft. Ambiance conviviale, food trucks et musique live au programme !",
                timezone.now() + timedelta(days=45),
                "Place du Marché, Paris 11ème",
                True,
            ),
        ]

        for title, slug, desc, date, location, published in events_data:
            Event.objects.get_or_create(
                slug=slug,
                defaults={
                    "title": title,
                    "description": desc,
                    "event_date": date,
                    "location": location,
                    "is_published": published,
                },
            )

        self.stdout.write(self.style.SUCCESS(
            f"Seed terminé : {Category.objects.count()} catégories, "
            f"{Product.objects.count()} produits, {Event.objects.count()} événements."
        ))
