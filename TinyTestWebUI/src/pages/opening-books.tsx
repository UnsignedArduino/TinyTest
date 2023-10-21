import Layout from "@/components/Layout";
import getAppProps, { AppProps } from "@/components/WithAppProps";
import React from "react";
import { APICallDirectAsUser } from "@/scripts/TinyTestServerAPI/APICall";

const pageName = "Opening books";

enum CompressionFormatEnum {
  NONE = "none",
  ZIP = "zip",
}

enum BookFormatEnum {
  PGN = "pgn",
  EPD = "epd",
}

type OpeningBookData = {
  id: number;
  name: string;
  compression_format: CompressionFormatEnum;
  book_format: BookFormatEnum;
};

type BookStatusState = "loading" | "fetched" | "error";

export default function OpeningBooks({ appProps }: { appProps: AppProps }) {
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

  React.useEffect(() => {
    refreshBooks();
  }, []);

  return (
    <Layout title={pageName} currentPage={pageName} appProps={appProps}>
      <>
        <h1>Opening books</h1>
        <p>
          You can view opening books that can be used in SPRTs in the table
          below!
        </p>
        <div className="alert alert-info" role="alert">
          Please be patient when downloading books!
        </div>
        <div className="table-responsive">
          <table className="table table-striped">
            <thead>
              <tr>
                <th scope="col">ID</th>
                <th scope="col">Name</th>
                <th scope="col">Book format</th>
                <th scope="col">Compression format</th>
                <th scope="col">File</th>
              </tr>
            </thead>
            <tbody>
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
                          <span className="placeholder col-2" />
                        </td>
                        <td>
                          <span className="placeholder col-2" />
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
                            <td>{book.book_format}</td>
                            <td>{book.compression_format}</td>
                            <td>
                              <a
                                className="btn btn-sm btn-secondary"
                                href={
                                  process.env.NEXT_PUBLIC_API_SERVER_URL +
                                  `/opening-books/content?book_id=${book.id}`
                                }
                                download={`${book.name}.${book.book_format}${
                                  book.compression_format ==
                                  CompressionFormatEnum.NONE
                                    ? ""
                                    : `.${book.compression_format}`
                                }`}
                              >
                                <i className="bi-download" />
                              </a>
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
      </>
    </Layout>
  );
}

export async function getStaticProps(): Promise<{
  props: { appProps: AppProps };
}> {
  return {
    props: {
      appProps: await getAppProps(),
    },
  };
}
