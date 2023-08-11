#----------------------------------------------------
# TODO
#----------------------------------------------------
# 

#----------------------------------------------------
# Imports
#----------------------------------------------------
import helper

#----------------------------------------------------
# Functions
#----------------------------------------------------
class XForce_Database():
    """ 
    on streamlit, "graph" / show the current_working_db data always.
    """
    def __init__(self) -> None:
        self._selected_db = None
        self._selected_db_filepath = None
        self._selected_db_length = None
        self._selected_db_headers = None
        self._selected_db_name = None

        self._current_working_db = None
        self._current_working_db_filepath = None
        self._current_working_db_length = None
        self._current_working_db_headers = None
    
        return None

    def fetch_db_names(self):
        file_names = helper.os.listdir(helper.RELATIVE_TO_APP_DATA)
        extracted_file_names = [i.split(".")[0] for i in file_names]
        return extracted_file_names

    def select_db(self, path: str="") -> None:
        
        df = helper.pd.read_csv(path)
        # IMPLEMENT IN COOP -> ADVANCED FILTER
        # to_parse = helper.COLUMNS_WITH_NESTED_DATA
        # for parsed in to_parse:
        #     df[parsed] = df[parsed].apply(lambda x: helper.eval_db_values(x))

        self._selected_db = df
        self._selected_db_filepath = path
        self._selected_db_length = len(df)
        self._selected_db_headers = df.columns.tolist()
        self._selected_db_name = path.split('/')[-1].split(".")[0]

        self._current_working_db = df
        self._current_working_db_length = len(df)
        self._current_working_db_headers = df.columns.tolist()

        # print(f"{self._selected_db_name} selected!")
        return None
    
    def clear_curr_db_filters(self) -> None:
        """ 
        # TODO documentation
        undoes all the filtering/sorting by returning the current working db ot the original state
        """
        self._current_working_db = self._selected_db
        self._current_working_db_filepath = self._selected_db_filepath
        self._current_working_db_length = self._selected_db_length
        self._current_working_db_headers = self._selected_db_headers

        print(f"All filters and sorts made on {self._selected_db_name} has been reset!")
        return None
    
    def get_selected_db(self):
        return self._selected_db
    
    def get_selected_db_filepath(self):
        return self._selected_db_filepath

    def get_selected_db_length(self):
        return self._selected_db_length

    def get_selected_db_headers(self):
        return self._selected_db_headers
    
    def get_selected_db_name(self):
        return self._selected_db_name
    
    def get_current_working_db(self):
        return self._current_working_db
    
    def set_current_working_db(self, df):
        self._current_working_db = df
        return None

    def get_current_working_db_length(self):
        return self._current_working_db_length
    
    def get_current_working_db_headers(self):
        return self._current_working_db_headers

    def new_db(self, target_db_name) -> None:
        """ 
        # TODO documentation
        creates a new, empty db for data population and automatically switches to that new one
        """
        print("From: new")
        if target_db_name in helper.RESERVED_DB_NAMES:
            raise IOError
        else:
            new_filepath = helper.relativify_to_app(target_db_name)
            print(new_filepath)
            try:
                df = helper.pd.DataFrame(columns=helper.MASTER_CSV_COLUMNS)
                df.to_csv(new_filepath, index=False)
                self.select_db(new_filepath)
                print(f"Switching over to {self.get_selected_db_name()}!")
            except:
                print("Failed to create new database.")
        return new_filepath
    
    def reset_curr_db(self) -> None:
        """
        # TODO documentation
        wipes the entries in the CURRENT WORKING db
        """
        print("By reseting or wiping a database, you are removing the entries within it but not deleting the database file itself.")
        new_filepath = self.get_selected_db_filepath()
        name = self.get_selected_db_name()
        if name in helper.PROTECTED_DB_NAMES:
            print(f"At the moment, resetting {self.get_selected_db_name()} is unadvised because it contains 11hr+ of pre-processed NLP data.")
        else:
            df = helper.pd.DataFrame(columns=helper.MASTER_CSV_COLUMNS)
            try:
                df.to_csv(new_filepath, index=False)
                self.select_db(new_filepath)
                print("resetted")
            except:
                print("Failed to reset/wipe.")
        return None

    def delete_curr_db(self) -> None:
        """ 
        # TODO documentation
        deletes the current specified db
        """
        print("By removing the file itself, this database will no longer appear in the selection dropdown.")
        new_filepath = self.get_selected_db_filepath()
        name = self.get_selected_db_name()
        if name in helper.RESERVED_DB_NAMES:
            print(f"{name} is currently reserved. You cannot create, overwrite, or delete a DB with this name.")
        else:
            try:
                helper.os.remove(new_filepath)
                self.select_db(helper.RELATIVE_TO_APP_DEFAULT_DB)
                print(f"Switching over to {self.get_selected_db_name()}!")
            except:
                print("Failed to delete.")
        return None
    
    def filter_curr_rows(self, start, end) -> None:
        df = self.get_current_working_db()
        df = df.iloc[start:end, :]
        self.set_current_working_db(df)
        return None
    
    def filter_curr_source(self, values: list=["ALL"]) -> None:
        """ 
        # TODO DOC
        filter on source
        """
        df = self.get_current_working_db()
        query_options = df["source"].unique()
        if values != ["ALL"]:
            for value in values:
                if value not in query_options:
                    print(f"{value} not found in query; allowed: {query_options}.")
                    return None
            expression = helper.generate_boolean_conditions("source", values)
            df = df[eval(expression)]
            self.set_current_working_db(df)
        return None
    
    def filter_curr_query(self, values: list=["ALL"]) -> None:
        """ 
        # TODO DOC
        filter on query
        """
        df = self.get_current_working_db()
        query_options = df["query"].unique()
        if values != ["ALL"]:
            for value in values:
                if value not in query_options:
                    print(f"{value} not found in query; allowed: {query_options}.")
                    return None
            expression = helper.generate_boolean_conditions("query", values)[1:-1]
            df = df[eval(expression)]
            self.set_current_working_db(df)
        return None

    def filter_curr_title(self, values: list=["ALL"], and_or_condition: int=0) -> None:
        """ 
        # TODO DOC
        filter on title
        """
        df = self.get_current_working_db()
        if values != ["ALL"]:
            expression = helper.generate_robust_boolean_conditions("title", values, and_or_condition)
            df = df[eval(expression)]
            self.set_current_working_db(df)
        return None
    
    def filter_curr_abstract(self, values: list=["ALL"], and_or_condition: int=0) -> None:
        """ 
        # TODO DOC
        filter on abs
        """
        df = self.get_current_working_db()
        if values != ["ALL"]:
            expression = helper.generate_robust_boolean_conditions("abstract", values, and_or_condition)
            df = df[eval(expression)]
            self.set_current_working_db(df)
        return None
    
    def filter_curr_author(self, values: list=["ALL"], and_or_condition: int=0) -> None:
        """ 
        # TODO DOC
        filter on author
        """
        df = self.get_current_working_db()
        if values != ["ALL"]:
            expression = helper.generate_robust_boolean_conditions("authors", values, and_or_condition)
            df = df[eval(expression)]
            self.set_current_working_db(df)
        return None
    
    def filter_curr_date(self, start: int=0, end: int=0) -> None:
        """ 
        # TODO DOC for COOP
        filter on date
        """
        return None

    def sort_curr_db(self, sort_on: str="published", is_ascending: bool=True, ) -> None:
        df = self.get_current_working_db()
        df.sort_values(sort_on, ascending=is_ascending, inplace=True)
        self.set_current_working_db(df)
        return None
    
    def dedupe_curr_db(self) -> None:
        """ 
        Manually remove duplicates between Scopus and Arxiv in current selected db.
        
        Returns -> None
            Current database is cleaned of duplicates via the "title" column.
        
        Example
            dedupe_curr_db()
        """
        print("This will remove all duplicates within the selected database.")
        df = self.get_selected_db()
        name = self.get_selected_db_name()

        pre_len = len(df)
        df = df[~df.duplicated("title")]
        post_len = len(df)
        print(f"Removed {pre_len - post_len} duplicates ({pre_len} -> {post_len})!")

        df.to_csv(helper.relativify_to_app(name), index=False)
        self.select_db(helper.relativify_to_app(name))

        return None

    def confirm_db(self) -> None:
        print("Confirming current filters/sorts. Will use this filtered/sorted data for graphing!")
        self.get_current_working_db().to_csv(helper.RELATIVE_TO_APP_DEFAULT_CURR_WORKING_DB)
        return None

    def skeleton(self) -> None:
        return None
    
#----------------------------------------------------
# Module Checking
#----------------------------------------------------
def main():
    pass

if __name__ == "__main__":
    main()