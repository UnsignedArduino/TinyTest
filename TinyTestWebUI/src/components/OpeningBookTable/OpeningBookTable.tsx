import { UserContext } from "@/components/contexts";
import { APICallDirectAsUser } from "@/scripts/TinyTestServerAPI/APICall";
import React from "react";
import AddOpeningBookRow from "@/components/OpeningBookTable/AddOpeningBookRow";
import DeleteOpeningBookButton from "@/components/OpeningBookTable/DeleteOpeningBookButton";

type OpeningBookData = {
  id: number;
  name: string;
};

type BookStatusState = "loading" | "fetched" | "error";

export default function OpeningBookTable() {
  const userContext = React.useContext(UserContext);

  const [bookStatus, setBookStatus] =
    React.useState<BookStatusState>("loading");
  const [books, setBooks] = React.useState<OpeningBookData[]>([]);

  function refreshBooks() {
    setBookStatus("loading");
    APICallDirectAsUser("/opening-books/all", "GET", undefined)
      .then((response) => {
        if (response.status != 200) {
          setBookStatus("error");
        } else {
          response.json().then((json) => {
            setBooks(json);
            setBookStatus("fetched");
          });
        }
      })
      .catch(() => {
        setBookStatus("error");
      });
  }

  const refreshOpeningBookRef = React.useRef(refreshBooks);

  React.useEffect(() => {
    refreshBooks();
  }, []);

  return (
    <div className="table-responsive">
      <table className="table table-striped">
        <thead>
          <tr>
            <th scope="col">ID</th>
            <th scope="col">Name</th>
            <th scope="col">File</th>
          </tr>
        </thead>
        <tbody>
          {userContext != null && userContext.admin ? (
            <AddOpeningBookRow
              apiToken={userContext!.apiToken}
              refreshBookCallbackRef={refreshOpeningBookRef}
            />
          ) : undefined}
          {(() => {
            switch (bookStatus) {
              case "loading":
                const loadingRow = (
                  <tr className="placeholder-glow">
                    <th scope="row">
                      <span className="placeholder col-3" />
                    </th>
                    <td>
                      <span className="placeholder col-9" />
                    </td>
                    <td>
                      <span className="placeholder col-6" />
                    </td>
                  </tr>
                );
                return (
                  <>
                    {loadingRow}
                    {loadingRow}
                    {loadingRow}
                  </>
                );
              case "fetched":
                return books.length > 0 ? (
                  books.map((book) => {
                    return (
                      <tr key={book.id}>
                        <th scope="row">{book.id}</th>
                        <td>{book.name}</td>
                        <td>
                          <a
                            className="btn btn-sm btn-secondary"
                            href={
                              process.env.NEXT_PUBLIC_API_SERVER_URL +
                              `/opening-books/content?book_id=${book.id}`
                            }
                            download={book.name}
                          >
                            <i className="bi-download" />
                          </a>
                          {userContext != null && userContext.admin ? (
                            <DeleteOpeningBookButton
                              id={book.id}
                              apiToken={userContext!.apiToken}
                              refreshBookCallbackRef={refreshOpeningBookRef}
                            />
                          ) : undefined}
                        </td>
                      </tr>
                    );
                  })
                ) : (
                  <tr>
                    <td colSpan={5}>
                      <div className="alert alert-info m-0" role="alert">
                        No books found!
                      </div>
                    </td>
                  </tr>
                );
              case "error":
                return (
                  <tr>
                    <td colSpan={5}>
                      <div className="alert alert-danger m-0" role="alert">
                        Error fetching opening books!
                      </div>
                    </td>
                  </tr>
                );
            }
          })()}
        </tbody>
      </table>
    </div>
  );
}
