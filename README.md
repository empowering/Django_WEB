# Web

Web Programming with Python(Flask && Django) and JavaScript

## Project 0 - Finance 
#### Flask & JavaScript & SQLite

Create a website via which users can “buy” and “sell” stocks.
1. Register 
    -  Allows a user to register for an account via a form
2. Quote ( API )
    -  Allows a user to look up a stock’s current price.
3. Buy 
    -  Enables a user to buy stocks within its budget.
4. Index
    -  Displays an HTML table summarizing, for the user currently logged in, which stocks the user owns, the numbers of shares owned, the current price of each stock, and the total value of each holding && user’s current cash balance along with a grand total (i.e., stocks’ total value plus cash).
5. Sell 
    -  Enables a user to sell shares of a stock of user's own.
6. History ( Pesonal Page )
    -  Displays an HTML table summarizing all of a user’s transactions ever, listing row by row each and every buy and every sell

- install requirements
```
pip3 install cs50
pip3 install flask-session
```


## Project 1 - Wiki 
#### Django
Design a Wikipedia-like online encyclopedia.

### Specification

1. Index Page
    -  wiki 목록 보여주기 및 상세페이지 연결
    -  검색 기능
    - 정확하게 일치하는 결과가 없는 경우 검색어를 포함한 페이지 목록 보여주기
2. Entry Page
    -  글 수정 
3. New Page
    -  해당 포맷을 md파일로 저장
4. Edit Page
    -  해당 페이지 수정
5. Markdown to HTML Conversion
    -  md파일 내용을 html syntax에 맞추어 반환
6. Random Page
    -  저장되어있는 wiki 중 랜덤으로 페이지 이동



## Project 2 - Commerce (auctions) 
#### Django & SQLite ( Only Backend )

Design an eBay-like e-commerce auction site that will allow users to post auction listings, place bids on listings, comment on those listings, and add listings to a “watchlist.”

### Specification

1. User
    -  Log-in / Log-out / Register
2. Listing
    -  Create / Edit / Delete Post
3. Detail Page
    -  Add to Favorites and view all in Watchlist
    -  Comment
    -  Bidding
        -  You can bid for the item <b> only when your call is higher than the current bidding price </b>
4. Category
    -  View the data according to the specific category
5. Django Admin
    -  createSuperuser
    -  View and manage DB



## Project 3 - Mail 
#### Django & Javascript 

Design a front-end for an email client that makes API calls to send and receive emails.

### Specification

1. Send Mail:
    -  make a POST request to /emails, passing in values for recipients, subject, and body
2. Mailbox: 
    -  Inbox / Sent mailbox / Archive
        -  make a GET request to /emails/<mailbox> to request the emails for a particular mailbox
        -  When a mailbox is visited, the application first queries the API for the latest emails in that mailbox.
        -  If the email is unread, it appears with a white background. If not, it appears with a gray background.
3. View Email:
    -  make a GET request to /emails/<email_id> to request the email
    -  Once the email has been clicked on, application marks the email as read. 
4. Archive and Unarchive:
    -  When viewing an Inbox email, the user is presented with a button that lets them archive the email. When viewing an Archive email, the user is presented with a button that lets them unarchive the email. 
5. Reply:
    -  When the user is presented with reply view, composition form is pre-filled with 
        -  the recipient field set to whoever sent the original email
        -  subject line begins with "Re:"
 
### Things to fix
- sent 메일함에는 archive 버튼 hide
- 자기 자신한테 보낸 메일 background gray
