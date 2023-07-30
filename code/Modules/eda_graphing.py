#----------------------------------------------------
# TODO
#----------------------------------------------------
# IMPORT eda graphign ipynb and add the todos here

#----------------------------------------------------
# Imports Checking
#----------------------------------------------------
import helper

#----------------------------------------------------
# Global Variable
#----------------------------------------------------
is_demo = True

#----------------------------------------------------
# Helper Class
#----------------------------------------------------
class TextNorm(helper.Normalize):
    """
    # TODO: finish documention
    Map a list of text values to the float range 0-1
    """

    def __init__(self, textvals, clip=False):
        self._clip = clip
        # if you want, clean text here, for duplicate, sorting, etc
        ltextvals = set(textvals)
        self.N = len(ltextvals)
        self.textmap = dict(
            [(text, float(i)/(self.N-1)) for i, text in enumerate(ltextvals)])
        self._vmin = 0
        self._vmax = 1

    def __call__(self, x, clip=None):
        ret = helper.ma.asarray([self.textmap.get(xkey, -1) for xkey in x])
        return ret

    def inverse(self, value):
        return ValueError("TextNorm is not invertible")
    
#----------------------------------------------------
# Graphing Class
#----------------------------------------------------
class XForce_Grapher():
    def __init__(self) -> None:
        self._data = None
        self._sources = None
        self._queries = None
        self._summary = None
        self._nlp_summary = None
        self._data_size = None
        if is_demo:
            self.load("../data/demo_db.csv")
        else:
            self.load("../data/complete_db.csv")
        return None

    def load(self, path: str) -> None:
        self.load_db(path)
        self.load_db_summary()
        self.load_nlp_summary()
        return None

    def peek_data(self):
        return self._data.head()
    
    def get_data(self):
        return self._data

    def get_sources(self):
        return self._sources

    def get_queries(self):
        return self._queries
    
    def get_summary(self):
        return self._summary
    
    def peek_nlp_summary(self):
        return self._nlp_summary.sort_values(by="abstract_word_count").reset_index().iloc[np.r_[0:5, -5:0]]

    def get_nlp_summary(self):
        return self._nlp_summary

    def set_data(self, path: str) -> None:
        self.load(path)
        return None

    def load_db(self, path: str) -> None:
        df = pd.read_csv(path)
        sources = list(set(df["source"].values.tolist()))
        sources.append("ALL")
        queries = list(set(df["query"].values.tolist()))
        queries.append("ALL")

        self._data = df
        self._data_size = len(df)
        self._sources = sources
        self._queries = queries
        return None

    def graph_pub_freq(self,
                       queries: list=["ALL"], 
                       sources: list=["ALL"],
                       country_mode: int=1) -> None:
        """
        # TODO Fix scopus date. Do not you run "ALL" for sources.
        # TODO Add country_mode

        Graphs the publishing frequency of papers in the database.

        queries -> list
            The given list of search queries (can be a 1-item list) that match database queries
            ALL: Considers all queries

        sources -> list
            The given list of search sources (can be a 1-item list) that match database sources
            ALL: Considers all sources

        country_mode -> int
            0: graphs the bars of the bar chart as normal bars
            1: graphs the bars of the bar chart as stacked bar charts corresponding to country of publishing institution

        Returns -> None
            Shows matplotlib graph of the published frequency
        
        Example
            grapher = XForce_Grapher()
            grapher.graph_pub_freq(["ALL"], ["ALL"], 1)
        """

        # Input Error Handling
        country_mode_options = {0,1}
        if country_mode not in country_mode_options:
            print(f"{country_mode} invalid, must be {country_mode_options}")
            return None

        for source in sources:
            if source not in self._sources:
                raise ValueError(f"{source} invalid, must be {self._sources}")
        
        for query in queries:
            if query not in self._queries:
                raise ValueError(f"{query} invalid, must be {self._queries}")

        # Load Data
        df = self._data.copy()
        
        # Filter Data
        title_sources, title_queries = ["ALL"], ["ALL"]
        if "ALL" not in sources:
            expression = helper.generate_boolean_conditions("source", sources)
            df = df[eval(expression)]
            title_sources = sources
        if "ALL" not in queries:
            expression = helper.generate_boolean_conditions("query", queries)
            df = df[eval(expression)]
            title_queries = queries
        
        # Data Setup
        dates_extract = df["published"].apply(lambda x: x.split('T')[0])
        dates = [datetime(int(i.split("-")[0]), int(i.split("-")[1]), int(i.split("-")[2])) for i in dates_extract]
        
        # Graph
        plt.title(f"Source: {title_sources}, Query: {title_queries}", fontsize=3)
        plt.suptitle(f"Publish Frequency within {len(dates)} Most Recent Papers")
        plt.xlabel("Publish Dates")
        plt.ylabel("Frequency")
        plt.grid("True")
        plt.xticks(rotation=45)
        plt.hist(dates, 25, alpha=.75)
        plt.tight_layout()
        plt.savefig(f"../images/pub_freq/pub_freq_{'_'.join(title_sources)}_{'_'.join(title_queries)}.png")
        plt.show()

        # Return
        return f"../images/pub_freq/pub_freq_{'_'.join(title_sources)}_{'_'.join(title_queries)}.png"

    def load_db_summary(self) -> None:
        """
        Generates the report table of the count of paper entries by query and by source and stores it in class attribute.

        Returns -> None
            Stores the report dataframe into class attribute.

        Example
            grapher = XForce_Grapher()
            grapher.load_db_summary()
        """
        df = self._data.copy()
        sources = self._sources.copy()
        queries = self._queries.copy()
        l = [["source"], queries]
        data_header = [item for sublist in l for item in sublist]
        data_rows = []
        for source in sources:
            data_row = [source]
            if source == "ALL":
                filtered_by_source_df = df
            else:
                filtered_by_source_df = df[df["source"] == source]
            for query in queries:
                filtered_by_query_df = filtered_by_source_df[filtered_by_source_df["query"] == query]
                data_row.append(len(filtered_by_query_df))
            data_rows.append(data_row)
        report = pd.DataFrame(data=data_rows, columns=data_header).iloc[:, :-1]
        self._summary = report
        return None
    
    def report_db_summary(self) -> None:
        """ 
        Prints a report table of the count of paper entries by query and by source.

        Returns -> None
            Both prints and returns the report dataframe.

        Example
            grapher = XForce_Grapher()
            grapher.report_db_summary()
        """
        print(self._summary)
        return None

    def graph_db_summary(self) -> str:
        """
        Graphs the report summary as a stacked barchart.

        Returns -> str
            Shows matplotlib graph of the report summary, and returns the generated plot path
        
        Example
            grapher = XForce_Grapher()
            grapher.graph_db_summary()
        """

        df = self._summary.copy()
        extract_counts = df.T.values.tolist()[1:-1] # -1 to remove the "ALL" from the category
        extract_queries = df.T.index.tolist()[1:-1]
        sources = df["source"]

        query_count_data = {}
        for i in range(len(extract_counts)):
            query_count_data[extract_queries[i]] = extract_counts[i]
        
        width = 0.5
        fig, ax = plt.subplots()
        bottom = np.zeros(3)

        for query, count in query_count_data.items():
            p = ax.bar(sources, count, width, label=query, bottom=bottom)
            bottom += count

        plt.title(f"Distribution of {self._data_size} Articles")
        plt.xlabel("Source")
        plt.ylabel("Counts")
        plt.grid("True")
        plt.legend(loc='upper left', bbox_to_anchor=(1,1))
        plt.tight_layout()
        plt.savefig(f"../images/db_summ/db_summ.png")
        plt.show()

        return "../images/db_summ/db_summ.png"
    
    def load_nlp_summary(self) -> None:
        """
        Creates, pre-processes, and saves the NLP summary report in class variable, which is ready for analytics.

        Returns -> None
            Saves the NLP summary report.
        
        Example
            grapher = XForce_Grapher()
            grapher.load_nlp_summary()
        """
        # Filtering
        df = self._data.copy()
        df = df[["source", "query", "published", "url", "title", "abstract"]]

        # Cleaning
        df.dropna(inplace=True)
        df.loc[:, "title"] = df.loc[:, "title"].map(lambda x: x.lower())
        df.loc[:, "abstract"] = df.loc[:, "abstract"].map(lambda x: x.lower())
        punctuation = ["\?", "‘", "’", "'", ",", "\.", "“", '"', "”", "\[", "\]", "\(", "\)", "\/"]
        for mark in punctuation:
            df.loc[:, "title"] = df.loc[:, "title"].str.replace(mark, "", regex=True)
            df.loc[:, "abstract"] = df.loc[:, "abstract"].str.replace(mark, "", regex=True)

        # Feature Engineering
        df["title_char_count"] = df.loc[:, "title"].map(lambda x: len(x))
        df["title_word_count"] = df.loc[:, "title"].map(lambda x: len(x.split(" ")))
        df["abstract_char_count"] = df.loc[:, "abstract"].map(lambda x: len(x))
        df["abstract_word_count"] = df.loc[:, "abstract"].map(lambda x: len(x.split(" ")))

        # Saving
        self._nlp_summary = df
        
        # Return
        return None
    
    def graph_text_freq(self,
                         queries: list=["ALL"], 
                         sources: list=["ALL"], 
                         text_mode: str="word", 
                         type_mode: str="abstract") -> str:
        """
        Graphs the text frequency (eg. character/word count of title/abstract) of indicated papers

        queries -> list
            The given list of search queries (can be a 1-item list) that match database queries
            ALL: Considers all queries

        sources -> list
            The given list of search sources (can be a 1-item list) that match database sources
            ALL: Considers all sources

        text_mode -> str
            Given type mode to filter on
            "char": Graphs via character count
            "word": Graphs via word count

        type_mode -> str
            Given type mode to filter on
            "title": Graphs on title
            "abstract": Graphs on abstract

        Returns -> str
            Shows matplotlib graph of the text counts, and returns the generated plot path
        
        Example
            grapher = XForce_Grapher()
            grapher.graph_text_freq(queries=["radiation", "plasmonics"], source=["arxiv"], text_mode="word", type_mode="abstract")
        """

        # Input Error Handling
        for source in sources:
            if source not in self._sources:
                raise ValueError(f"{source} invalid, must be {self._sources}")
        
        for query in queries:
            if query not in self._queries:
                raise ValueError(f"{query} invalid, must be {self._queries}")

        text_mode_options = {"char", "word"}
        if text_mode not in text_mode_options:
            raise ValueError(f"{text_mode} invalid; must be {text_mode_options}")

        type_mode_options = {"title", "abstract"}
        if type_mode not in type_mode_options:
            raise ValueError(f"{type_mode} invalid; must be {type_mode_options}")

        # Load Data
        df = self._nlp_summary.copy()
        
        # Filter Data
        title_sources, title_queries = ["ALL"], ["ALL"]
        if "ALL" not in sources:
            expression = helper.generate_boolean_conditions("source", sources)
            df = df[eval(expression)]
            title_sources = sources
        if "ALL" not in queries:
            expression = helper.generate_boolean_conditions("query", queries)
            df = df[eval(expression)]
            title_queries = queries
        else:
            queries = self._queries[:-1]

        # Data Setup
        expression = f"{type_mode}_{text_mode}_count"
        graph_data = []
        for query in queries:
            graph_data.append(df[df["query"] == query][expression])

        # Graphing
        plt.title(f"Source: {title_sources}, Query: {title_queries}")
        plt.suptitle(f"Summary Statistics of {type_mode.title()} {text_mode.title()} Count by Specified Papers")
        plt.xlabel("Query")
        plt.ylabel("Count")
        plt.grid("True")
        plt.xticks(rotation=45)
        plt.boxplot(graph_data, positions=np.array(range(len(graph_data)))*2.0, sym='', widths=1.5)
        plt.xticks(range(0, len(queries)*2, 2), queries, rotation=45)
        plt.tight_layout()
        plt.savefig(f"../images/text_freq/text_freq_{'_'.join(title_sources)}_{'_'.join(title_queries)}.png")
        plt.show()

        return f"../images/text_freq/text_freq_{'_'.join(title_sources)}_{'_'.join(title_queries)}.png"
    
    def graph_keyword_freq(self,
                           queries: list=["ALL"], 
                           sources: list=["ALL"], 
                           type_mode: str="abstract", 
                           k: int=15, 
                           n_gram: int=1, 
                           stop_words: set=helper.MASTER_STOP_WORDS) -> str:
        """
        Graphs the keyword frequency of the specified papers. 

        queries -> list
            The given list of search queries (can be a 1-item list) that match database queries
            ALL: Considers all queries

        sources -> list
            The given list of search sources (can be a 1-item list) that match database sources
            ALL: Considers all sources

        type_mode -> str
            Given type mode to filter on
            "title": Graphs on title
            "abstract": Graphs on abstract

        k -> int
            The number of top n-grams to be graphed

        n_gram -> int
            The n-grams to graph on

        stop_words -> set
            The set of stop_words to use in the CountVectorizer()

        Returns -> str
            Shows matplotlib graph of the text counts, and returns the generated plot path
        
        Example
            grapher = XForce_Grapher()
            grapher.graph_text_count(queries=["radiation", "plasmonics"], source="arxiv", type_mode="abstract", k=15, n_grams=1)
        """

        # Input Error Handling
        for source in sources:
            if source not in self._sources:
                raise ValueError(f"{source} invalid, must be {self._sources}")
        
        for query in queries:
            if query not in self._queries:
                raise ValueError(f"{query} invalid, must be {self._queries}")

        type_mode_options = {"title", "abstract"}
        if type_mode not in type_mode_options:
            raise ValueError(f"{type_mode} invalid; must be {type_mode_options}")

        # Load Data
        df = self._nlp_summary.copy()
        
        # Filter Data
        title_sources, title_queries = ["ALL"], ["ALL"]
        if "ALL" not in sources:
            expression = helper.generate_boolean_conditions("source", sources)
            df = df[eval(expression)]
            title_sources = sources
        if "ALL" not in queries:
            expression = helper.generate_boolean_conditions("query", queries)
            df = df[eval(expression)]
            title_queries = queries
        else:
            queries = self._queries[:-1]

        X = df.loc[:, type_mode]
        cvec = CountVectorizer(stop_words=stop_words, ngram_range=(n_gram, n_gram))
        X_cvec_dense = cvec.fit_transform(X).todense()
        X_cvec_df = pd.DataFrame(X_cvec_dense, columns=cvec.get_feature_names_out())

        # graphing
        graph_data = X_cvec_df.sum().sort_values(ascending=False).head(k)
        plt.title(f"Source: {title_sources}, Query: {title_queries}")
        plt.suptitle(f"Top {k} Most Common {n_gram}-Grams in Papers from Given Queries")
        plt.xlabel("Count")
        plt.xticks(rotation=90)
        plt.ylabel("Tokens")
        plt.grid(True)
        plt.barh(graph_data.index[::-1], graph_data.values[::-1], alpha=0.5)

        # saving
        plt.tight_layout()
        plt.savefig(f"../images/keyword_freq/keyword_freq_{'_'.join(title_sources)}_{'_'.join(title_queries)}.png")
        plt.show()

        return f"../images/keyword_freq/keyword_freq_{'_'.join(title_sources)}_{'_'.join(title_queries)}.png"
    

#----------------------------------------------------
# Module Checking
#----------------------------------------------------
def main():
    return None

if __name__ == "__main__":
    main()