import { loadingNotify } from "@/components/Notifications";
import { APICallDirectAsUser } from "@/scripts/TinyTestServerAPI/APICall";
import React from "react";

type DeletingStatusState = "deleting" | "deleted" | "error" | "none";

export default function DeleteOpeningBookButton({
  id,
  apiToken,
  refreshBookCallbackRef,
}: {
  id: number;
  apiToken: string;
  refreshBookCallbackRef: React.MutableRefObject<() => void>;
}) {
  const [deleteStatus, setDeleteStatus] =
    React.useState<DeletingStatusState>("none");

  function deleteOpeningBook(id: number) {
    console.log(`Deleting opening book ${id}`);
    setDeleteStatus("deleting");
    const { successCallback, errorCallback } = loadingNotify(
      "Deleting opening book...",
      "Successfully deleted opening book!",
      "Failed to delete opening book!",
      "Canceled deleting opening book!",
    );
    setTimeout(() => {
      APICallDirectAsUser(
        `/opening-books?book_id=${id}`,
        "DELETE",
        null,
        apiToken,
      )
        .then((response) => {
          if (response.status !== 204) {
            throw new Error("Error deleting opening book!");
          }
          successCallback();
          setDeleteStatus("deleted");
        })
        .catch(() => {
          errorCallback();
          setDeleteStatus("error");
        })
        .finally(() => {
          refreshBookCallbackRef.current();
        });
    }, 1000);
  }

  return (
    <button
      className="btn btn-sm btn-danger ms-1"
      disabled={deleteStatus == "deleting"}
      onClick={() => {
        deleteOpeningBook(id);
      }}
    >
      {(() => {
        switch (deleteStatus) {
          case "none":
            return <i className="bi-trash" />;
          case "deleting":
            return (
              <div className="spinner-border spinner-border-sm" role="status">
                <span className="visually-hidden">Deleting...</span>
              </div>
            );
          case "deleted":
            return <i className="bi-check-lg" />;
          case "error":
            return <i className="bi-x-lg" />;
        }
      })()}
    </button>
  );
}
