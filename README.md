Qiita clone
====

<a href="https://qiita.com/" target="_blank">Qiita</a>のクローンアプリです。

## Description
Djangoで実装されています。

## Requirement
Python3.6  
Django==2.1.2  
pytz==2018.6

## Usage
1. Githubからリポジトリをクローン
```
$ git clone https://github.com/Takumetal/qiita-clone.git
```
2. プロジェクトディレクトリに入る
```
$ cd qiita-clone
```
3. pipを使用して、必要なライブラリをインストール
```
$ pip install -r requirements.txt 
```
4. データベースを構築するためにマイグレーションファイルを生成
```
$ python manage.py makemigrations
```
5. 生成したマイグレーションファイルを使用して実際にデータベースを作成
```
$ python manage.py migrate
```
6. データベースにデータを投入
```
$ python manage.py loaddata fixtures/db.json
```
7. メッセージファイルをコンパイルし、多言語化
```
$ python manage.py compilemessages
```
<font color="red">*※Windows上でcompilemessagesするためには、GNU gettext toolsが必要です。*</font>

8. Djangoの開発サーバーを起動
```
$ python manage.py runserver
```
9. ブラウザで以下のURLにアクセス
```
http://127.0.0.1:8000
```

### デフォルトで用意されているユーザ情報
以下のユーザを使用して、ログインすることができます。
```
・administrator
    ・email: administrator@qiitaclone.com
    ・password: administrator
・user1
    ・email: user1@qiitaclone.com
    ・password: user1
・user2
    ・email: user2@qiitaclone.com
    ・password: user2
・user3
    ・email: user3@qiitaclone.com
    ・password: user3
・user4
    ・email: user4@qiitaclone.com
    ・password: user4
・user5
    ・email: user5@qiitaclone.com
    ・password: user5
```

## Licence
MIT

## Author
[Takumetal](https://github.com/Takumetal)
