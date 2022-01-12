# ximport

Once there was import, now there's ximport

## Instructions

1. Install requirements

```
brew tap microsoft/mssql-preview https://github.com/Microsoft/homebrew-mssql-preview
brew install msodbcsql mssql-tools freetds
```

2. Check the location of `freetds.conf` by running `tsql -C`

3. Add servers to the freetds.conf file as follows:
```
[MYMSSQL]
host = mssqlhost.xyz.com
port = 1433
tds version = 7.3
```