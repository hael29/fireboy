# Fireboy & Watergirl
Dokumentace k naší hře:
Na hraní naší hry je nutné míti instalovaný Python a nějaký programovací software, pro příklad IDLE nebo VS Code. Jelikož naše hra využívá knihovnu Pygame, je nutné si ji instalovat. Ve VS Code je třeba do terminálu zadat příkaz 'pip install pygame'. V IDLE se pak tento příkaz musí zadat do příkazového řádku Windows.
Hra využívá spousty externích souborů, obrázků a zvuků, pro komfort tedy doporučujeme stáhnout si celou složku 'fireboy' a nic v ní neměnit. Hlavní soubor se jmenuje 'pokus.py'. Stačí spustit pouze ten, program si sám bere funkce ze souborů zbylých.
Po spuštění se ocitnete na hlavním menu. Z něj jde pokračovat do menu s levely, v němž narazíte na 10 hratelných levelů různých obtížností. Můžete hrát kterýkoli level bez omezení, kolikrát je libo.
V každém levelu budou vždy naši protagonisté - Fireboy a Watergirl, tedy Ohýnek a Voděnka. Jejich cílem je spolupracovat a z levelu utéct - učiní tak, když se oba dostanou ke kulatým dveřím na konci. Ale pozor - jeden bez druhého nemůže odejít a smrt byť jen jednoho znamená restart celého levelu. Ohýnek se ovládá pomocí kláves W, A, D. Voděnka se ovládá pomocí šipek nahoru, doleva, doprava.
V levelu můžou být různé kapaliny - láva, voda a jed. Lávou může Ohýnek projít, ale Voděnku zabíjí. Naopak, Voděnka smí do vody, ale Ohýnek ne. Jed zabíjí oba dva.
Cílem levelu tedy je dostat oba hrdiny k jejich východu.

Ve složce se také nachází soubor 'delani_levelu.py'. Tento soubor lze spustit a využít na vlastní grafické dělání levelu. Po spuštění se vás program zeptá, který soubor otevřít. Zadáte například 'level_1.txt'. Otevře se okno kde lze měnit první level. Pomocí různých tlačítek se zakreslují různé věci, pomocí klávesy N se maže. Konkrétní klávesy a jejich využití vám program vypíše do terminálu hned po spuštění. Nový level uložíte tak, že program zavřete pomocí křížku v rohu. 'level_1.txt' se tedy aktualizoval a po novém spuštění hlavního souboru bude první level jiný.

EDIT: Zjistili jsme, že je nutné si složku fireboy někam uložit/přesunout. Program nebude fungovat, necháte-li ho v zazipované složce, do které jste se dostali dvojitým kliknutím.
