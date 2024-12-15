import requests
import csv

user_id = 1

def load_rating() -> None:
    my_good_read_ratings = []
    my_ratings = requests.get(f"https://api.fantlab.ru/user/{user_id}/marks?sort=autor&type=all&page=1").json()["items"]
    print(f"Total found{len(my_ratings)}")
    for rating in my_ratings:
        # uncomment if throttling encountered
        # sleep(0.2)
        work = requests.get(f"https://api.fantlab.ru/work/{rating['work_id']}/extended").json()
        work_name_ru = work["work_name"]
        edition_info = work["editions_blocks"]
        for edition_info_id, edition_info in edition_info.items():
            if (edition_info["block"] == "paper"
                    and edition_info["title"] != "Издания"
                    and edition_info["title"] != "Аудиокниги"
                    and edition_info["title"] != "Электронные издания" ):
                for single_edition_info in edition_info["list"]:
                    if single_edition_info["name"] == work_name_ru:
                        my_good_read_ratings.append({
                            "Title": rating["work_name_orig"],
                            "Author": rating["work_author_orig"],
                            "My Rating": rating["mark"] / 2.0,
                            "Date Read": rating["mark_date_iso"],
                            "Shelves": "Read",
                            "ISBN": single_edition_info["isbn"],
                        })
                        break
            else:
                print(f"Skipped: {edition_info}")
                print("\n\n")


        with open('my_goodread_ratings_1_skipped.csv', mode='w', newline='') as file:

            writer = csv.DictWriter(file, fieldnames=["Title", "Author", "My Rating", "Date Read", "Shelves", "ISBN"])
            writer.writeheader()
            for my_goodread_rating in my_good_read_ratings:
                writer.writerow(my_goodread_rating)

if __name__ == '__main__':
   load_rating()