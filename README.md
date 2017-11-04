# fb2-mixer

Utility for blinded books reading.

Allows to mix and anonymise bulk of fb2 files.

Usage:

```
./run.py <input directory> <output directory>
```

The utility:

* shuffles files list,
* removes title and author information from meta-data,
* removes some of heading lines if they contain book title or author name,
* removes annotation and epigraph
* removes images,
* adds author information and book's title to the end of the text,
* randomly extends file size.

Note: all files will be converted to fb2.zip, UTF-8 charset.
