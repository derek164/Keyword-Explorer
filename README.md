# 📚 Keyword-Explorer

This application is meant for students and researchers to explore their areas of interest. With a given keyword, you can start by inspecting its usage over a given period of time. You can then dive deeper by viewing the top publications and the top contributors to a research area, as well as their bodies of relevant work, over the same period. From here, clicking on a title will open the publication in an online academic journal where you can quickly preview the abstract. If you come across a particularly interesting publication, you can save it for later by adding it to your favorites. While browsing, similar keywords will be recommended to you under the search bar as an avenue for exploration, and all publications will be presented with their associated keywords as well. Last but not least, all keywords have been made clickable to further your experience in learning and exploration! 



## Installation

### Dependencies

- Local version of `academicworld` database on MySQL, MongoDB, and Neo4j
- Password is set to `test_root` for both MySQL and Neo4j
- Graph Data Science library is installed on Neo4j ([Installation Guide](https://neo4j.com/docs/graph-data-science/current/installation/neo4j-desktop/))

### Setup

Create virtual environment with required python dependencies and load data objects specific to our project.
```{zsh}
make install
```

## Usage

Start the web application, then visit [http://localhost:8050/](http://localhost:8050/) to view.
```{zsh}
make app
```

## Design
This is a Single Page Application (SPA), which means the server sends what you need with each click, and the browser renders that information without the need to reload the page again. With that said, we have the client layer that enables communication between the interface and browser to facilitate user interaction, the application layer that processes browser requests and executes the associated logic to access relevant data, and the database layer that manages all the data and responds to requests from the application layer. In essence, we have the typical Model–View–Controller (MVC) architectural pattern for user interfaces. In this case, it is notable that there are three database servers in the database layer: MySQL, MongoDB, and Neo4j.

## Implementation
For the database layer, supported python drivers are used for each of the databases to establish connections and execute transactions. The drivers are then wrapped in python classes to form clients encapsulating data access and retrieval. The client and application layers were accomplished with the use of Dash, which is a python framework that simplifies the creation of interactive web applications. It takes care of generating JavaScript code for the UI elements as well as the Web API to create and update the content of the application in the browser. Lastly, we added some CSS code for styling the webpage.

## Widgets
1. Keyword Dropdown + Date Range Selector
    > <br> Database: <b>MySQL</b> <br>
    > Retrieve the list of all keywords. When values are selected, they are applied to the entire webpage. 
    > <details><summary><code>click to view code</code></summary> https://github.com/CS411DSO-SP23/DerekZhang_MeeraSrinivasan/blob/670df93e4cf5036243092f17f69b9a831c7d79b1/src/database/mysql/query.py#L50-L53 </details>
2. Similar Keywords
    > <br> Database: <b>Neo4j</b> <br>
    > Recommends five keywords most similar to the selected keyword based on weighted co-occurrence. This is both a query and an update widget. More details are discussed in the <a href="https://github.com/CS411DSO-SP23/Keyword-Explorer/tree/main#database-techniques">Database Techniques</a> section below. 
    > <details><summary><code>click to view code</code></summary> https://github.com/CS411DSO-SP23/DerekZhang_MeeraSrinivasan/blob/146528ec39b3fa61aea46236409be96159086eb7/src/database/neo4j/query.py#L13-L31 </details>
3. Keyword Usage Chart
    > <br> Database: <b>MongoDB</b> <br>
    > Displays the number of publications, the number of citations, and the number of keyword-relevant citations (KRC) for the selected keyword. This is a query widget. 
    > <details><summary><code>click to view code</code></summary> https://github.com/CS411DSO-SP23/DerekZhang_MeeraSrinivasan/blob/03ce18518de494d4ef8801a07a1bdde03567852c/src/database/mongo/query.py#L137-L173 </details>
4. Top Publications Tab
    > <br> Database: <b>Neo4j</b> <br>
    > Display publications ranked by KRC <i>w.r.t</i> the selected keyword. This is a query widget. 
    > <details><summary><code>click to view code</code></summary> https://github.com/CS411DSO-SP23/DerekZhang_MeeraSrinivasan/blob/146528ec39b3fa61aea46236409be96159086eb7/src/database/neo4j/query.py#L34-L44 </details>
5. Top Universities Tab
    > <br> Database: <b>Neo4j</b> <br>
    > Provide a dropdown of universities, ranked by aggregate KRC <i>w.r.t</i> the selected keyword. When a university is selected, display publications ranked by KRC <i>w.r.t</i> the selected keyword in which at least one of the university's faculty members is a collaborator. This is a query widget. 
    > <details><summary><code>click to view code</code></summary> https://github.com/CS411DSO-SP23/DerekZhang_MeeraSrinivasan/blob/146528ec39b3fa61aea46236409be96159086eb7/src/database/neo4j/query.py#L47-L57 https://github.com/CS411DSO-SP23/DerekZhang_MeeraSrinivasan/blob/146528ec39b3fa61aea46236409be96159086eb7/src/database/neo4j/query.py#L60-L73 </details>
6. Top Researchers Tab
    > <br> Database: <b>Neo4j</b> <br>
    > Provide a dropdown of researchers, ranked by aggregate KRC <i>w.r.t</i> the selected keyword. When a researcher is selected, display publications ranked by KRC <i>w.r.t</i> the selected keyword in which the researcher is a collaborator. This is a query widget. 
    > <details><summary><code>click to view code</code></summary> https://github.com/CS411DSO-SP23/DerekZhang_MeeraSrinivasan/blob/146528ec39b3fa61aea46236409be96159086eb7/src/database/neo4j/query.py#L76-L86 https://github.com/CS411DSO-SP23/DerekZhang_MeeraSrinivasan/blob/146528ec39b3fa61aea46236409be96159086eb7/src/database/neo4j/query.py#L89-L100 </details>
7. Favorites Buttons + Tab
    > <br> Database: <b>MySQL</b> <br>
    > Allow users to favorite publications by clicking on the star-shaped button to the left of each title. Each time a publication is favorited or unfavorited, the change will be reflected in the MySQL `favorites` table. The favorites tab will query the `favorites` table to display your favorite publications. As such, this is both a query and an update widget. More details are discussed in the <a href="https://github.com/CS411DSO-SP23/Keyword-Explorer/tree/main#database-techniques">Database Techniques</a> section below. 
    > <details><summary><code>click to view code</code></summary> https://github.com/CS411DSO-SP23/DerekZhang_MeeraSrinivasan/blob/e8f7adfb138a5f32620e4a0286ca55e03f29e246/src/database/prepared/query.py#L30-L33 https://github.com/CS411DSO-SP23/DerekZhang_MeeraSrinivasan/blob/e8f7adfb138a5f32620e4a0286ca55e03f29e246/src/database/prepared/query.py#L36-L39 https://github.com/CS411DSO-SP23/DerekZhang_MeeraSrinivasan/blob/e8f7adfb138a5f32620e4a0286ca55e03f29e246/src/database/prepared/query.py#L42-L45 </details>
8. Keyword Buttons
    > <br> Database: <b>Neo4j</b> <br>
    > Display all keywords associated with a publication in order of relevancy. Allow users to click on any of the keywords displayed on the webpage to select a new keyword. Doing so will apply the selection to the entire webpage. 
    > <details><summary><code>click to view code</code></summary> https://github.com/CS411DSO-SP23/DerekZhang_MeeraSrinivasan/blob/146528ec39b3fa61aea46236409be96159086eb7/src/database/neo4j/query.py#L103-L109 </details>

## Database Techniques
1. REST API for accessing databases
    > A REST API is mainly used to help users communicate with the database server through the webpage. Since our application can interact with data through the webpage, passing data between our Dash application and the database layer via python driver classes, it fulfills the requirements for this database technique.
    > <details><summary><code>click to view code</code></summary> https://github.com/CS411DSO-SP23/DerekZhang_MeeraSrinivasan/blob/815b0ae3042eb65e04fa8e56a801b2b0d4ba7630/src/api.py#L6-L131 https://github.com/CS411DSO-SP23/DerekZhang_MeeraSrinivasan/blob/815b0ae3042eb65e04fa8e56a801b2b0d4ba7630/src/app.py#L12-L14 </details>
2. View
    > In order to find similar keywords, we computed the weighted Jaccard similarity between the selected keyword and all other keywords. In order to run the [Node Similarity](https://neo4j.com/docs/graph-data-science/current/algorithms/node-similarity/) algorithm in Neo4j, we created a graph projection of keywords and publications. According to the [documentation](https://neo4j.com/docs/graph-data-science/current/management-ops/graph-catalog-ops/#:~:text=Graph%20algorithms%20run%20on%20a,aggregated%2C%20topological%20and%20property%20information), "A graph projection can be seen as a materialized view over the stored graph", so our application fulfills the requirements for this database technique.
    > <details><summary><code>click to view code</code></summary> https://github.com/CS411DSO-SP23/DerekZhang_MeeraSrinivasan/blob/146528ec39b3fa61aea46236409be96159086eb7/src/api.py#L34-L44 </details>
3. Prepared statements
    > We anticipated that one of the most common requests on our webpage would be to favorite and unfavorite publications, so we used prepared statements with [MySQLCursorPrepared](https://dev.mysql.com/doc/connector-python/en/connector-python-api-mysqlcursorprepared.html) to increase performance and security for these operations. We also used prepared statements to rapidly insert data scraped from the CrossRef API into MySQL. There is less overhead when using this database technique because statements do not need to be repeatedly parsed. Additionally, if our application was deployed, there would also be protection against SQL injection attacks since placeholders are used in place of directly writing values into the statements when parameterizing prepared statements.
    > <details><summary><code>click to view code</code></summary> https://github.com/CS411DSO-SP23/DerekZhang_MeeraSrinivasan/blob/815b0ae3042eb65e04fa8e56a801b2b0d4ba7630/src/database/prepared/client.py#L1-L32 </details>

## Extra Capabilities
### Publication links
> This capability is an instance of *external data sourcing*. We scraped the [CrossRef REST API](https://www.crossref.org/documentation/retrieve-metadata/rest-api/) for high probability matches between publication/faculty combinations in our `academicworld` with objects in the CrossRef registry. In terms of effort, it took 30-40 hours to work out the code for parallelizing the API requests, developing a proxy pool, and storing results in a thread-safe manner. This was necessary to collect a large amount of data from a free, public API without getting rate-limited. From there, it took 10 hours to collect the data. Once the data was collected, it then took another 10+ hours to find the best strategy for incorporating this data into our backend, implement those steps, and then link everything up to the frontend.
> <br><details><summary><code>click to view code</code></summary> https://github.com/CS411DSO-SP23/DerekZhang_MeeraSrinivasan/blob/815b0ae3042eb65e04fa8e56a801b2b0d4ba7630/src/crossref.py#L1-L238 https://github.com/CS411DSO-SP23/DerekZhang_MeeraSrinivasan/blob/815b0ae3042eb65e04fa8e56a801b2b0d4ba7630/src/proxy.py#L1-L209 </details>
> <br> This capability also makes use of <i>multi-database querying</i>. Since many records were rejected by MySQL when importing the <code>academicworld</code> data, we decided to query most of the data relating to publications from Neo4j. Meanwhile, we loaded the CrossRef links to MySQL for speed and convenience. In order to present only those publications for which we found links, we needed a way to filter publication result sets from Neo4j against the links stored in MySQL at runtime. In order to accomplish this objective, we check whether each publication is linked or not using the <code>publication_is_linked()</code> method before rendering the html component for that publication in the <code>generate_publication_list()</code> method. <br>
><details><summary><code>click to view code</code></summary> https://github.com/CS411DSO-SP23/DerekZhang_MeeraSrinivasan/blob/c9459d53356fc82e38b680733dfd84397353f1ad/src/database/prepared/query.py#L81-L86 https://github.com/CS411DSO-SP23/DerekZhang_MeeraSrinivasan/blob/c9459d53356fc82e38b680733dfd84397353f1ad/src/api.py#L109-L111 https://github.com/CS411DSO-SP23/DerekZhang_MeeraSrinivasan/blob/c9459d53356fc82e38b680733dfd84397353f1ad/src/app.py#L35-L41 </details>
> <br> I think this feature is cool because we are now able to provide (mostly) working links to online academic journals from our website. This makes our application much more viable for actually exploring scientific literature, which is true to our objectives because it facilitates learning.
