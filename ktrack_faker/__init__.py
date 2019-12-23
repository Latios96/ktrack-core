import json
import os

import attr
import faker
from faker.providers import BaseProvider


def load_data():
    json_path = os.path.join(os.path.dirname(__file__), "data.json")
    with open(json_path, "rb") as f:
        return json.load(f)


class ProjectNames(BaseProvider):
    _data = load_data()

    def client_name(self):
        return self.random_element(self._data)["client_name"]

    def project_name(self):
        return self.random_element(self._data)["project_name"]

    def full_project_name(self):
        return u"{} {}".format(self.client_name(), self.project_name())


class Movies(BaseProvider):
    _movie_names = ["Agent 327", "Spring", "Cosmos Laundromat"]

    def movie(self):
        return self.random_element(self._movie_names)


class ShotNames(BaseProvider):
    def shot_name(self):
        return "shot{}".format(str(self.random_number(1)).zfill(2) + "0")


@attr.s(frozen=True)
class Asset(object):
    name = attr.ib(type=str)
    type = attr.ib(type=str)


class Assets(BaseProvider):
    assets = {
        "Agent 327": [
            Asset(type="character", name="Agent 327"),
            Asset(type="character", name="Barber"),
            Asset(type="character", name="Boris Kloris"),
            Asset(type="character", name="Doctor"),
            Asset(type="character", name="Pigeon"),
            Asset(type="character", name="Victim"),
            Asset(type="character", name="Wu Manchu"),
            Asset(type="prop", name="Razor Figurine"),
            Asset(type="prop", name="Hairclipper Figurine"),
            Asset(type="prop", name="Barbershop furniture collection"),
            Asset(type="prop", name="Hairdryer"),
            Asset(type="prop", name="Open & Closed Sign"),
            Asset(type="prop", name="Barbershop Picture Frames"),
            Asset(type="prop", name="Surgeon Equipment"),
            Asset(type="prop", name="Umbrellas"),
            Asset(type="prop", name="Books"),
            Asset(type="prop", name="Bottles and jars"),
            Asset(type="prop", name="Thermal Lances"),
            Asset(type="prop", name="3 pairs of scissors"),
            Asset(type="prop", name="Razor Blade"),
            Asset(type="prop", name="Binoculars"),
        ],
        "Spring": [
            Asset(type="character", name="Spring"),
            Asset(type="character", name="Autumn"),
            Asset(type="character", name="Alpha"),
            Asset(type="character", name="Betas"),
            Asset(type="prop", name="Chimes"),
            Asset(type="prop", name="Icicles"),
            Asset(type="prop", name="Pillar"),
            Asset(type="prop", name="Plants"),
            Asset(type="prop", name="Rocks"),
            Asset(type="prop", name="Staff"),
            Asset(type="prop", name="Trees"),
        ],
        "Cosmos Laundromat": [
            Asset(type="character", name="Victor"),
            Asset(type="character", name="Franck Sheep"),
            Asset(type="character", name="Franck Caterpillar"),
            Asset(type="environment", name="Island"),
            Asset(type="prop", name="Cassette Player"),
            Asset(type="prop", name="Branch"),
            Asset(type="prop", name="Plants and Rocks Collection"),
            Asset(type="prop", name="Plants"),
            Asset(type="prop", name="Rocks"),
            Asset(type="prop", name="Staff"),
            Asset(type="prop", name="Trees"),
        ],
    }

    def asset(self, movie=None):
        if movie:
            movie_asset = self.assets.get(movie)
            if movie_asset:
                return self.random_element(movie_asset)

        return Asset(name=faker.Faker().name(), type="character")


def create_fake():
    fake = faker.Faker()

    fake.add_provider(Movies)
    fake.add_provider(ShotNames)
    fake.add_provider(Assets)
    fake.add_provider(ProjectNames)

    return fake
