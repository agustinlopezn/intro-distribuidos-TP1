echo "Photo1mb"
for i in {1..10}; do python3 upload.py -s files/source/photo1mb.jpg -n photo1mb.jpg -q; sleep 2; done
echo "Photo5mb"
for i in {1..10}; do python3 upload.py -s files/source/photo5mb.jpg -n photo5mb.jpg -q; sleep 2; done
echo "Libro"
for i in {1..10}; do python3 upload.py -s files/source/libro.pdf -n libro.pdf -q; sleep 2; done
echo "Librox2"
for i in {1..10}; do python3 upload.py -s files/source/librox2.pdf -n librox2.pdf -q; sleep 2; done
echo "Librox3"
for i in {1..10}; do python3 upload.py -s files/source/librox3.pdf -n librox3.pdf -q; sleep 2; done


echo "Photo1mb"
for i in {1..10}; do python3 download.py -n photo1mb.jpg -q; sleep 2; done
echo "Photo5mb"
for i in {1..10}; do python3 download.py -n photo5mb.jpg -q; sleep 2; done
echo "Libro"
for i in {1..10}; do python3 download.py -n libro.pdf -q; sleep 2; done
echo "Librox2"
for i in {1..10}; do python3 download.py -n librox2.pdf -q; done
echo "Librox3"
for i in {1..10}; do python3 download.py -n librox3.pdf -q; done
