import { loadingNotify } from "@/components/Notifications";
import {
  APICallDirectAsUser,
  FormDataCallDirectAsUser,
} from "@/scripts/TinyTestServerAPI/APICall";
import React from "react";

type UploadStatusState = "uploading" | "uploaded" | "error" | "none";

export default function AddOpeningBookRow({
  apiToken,
  refreshBookCallbackRef,
}: {
  apiToken: string;
  refreshBookCallbackRef: React.MutableRefObject<() => void>;
}) {
  const [file, setFile] = React.useState<File | null>();
  const [uploadStatus, setUploadStatus] =
    React.useState<UploadStatusState>("none");
  const resetUploadIconTimeoutRef = React.useRef<number | undefined>();

  function uploadOpeningBook() {
    clearTimeout(resetUploadIconTimeoutRef.current);
    console.log(`Uploading opening book ${file!.name}`);
    setUploadStatus("uploading");
    const { successCallback, errorCallback } = loadingNotify(
      "Uploading opening book...",
      "Successfully uploaded opening book!",
      "Failed to upload opening book!",
      "Canceled uploading opening book!",
    );
    setTimeout(() => {
      APICallDirectAsUser(
        "/opening-books",
        "POST",
        JSON.stringify({ id: 0, name: file!.name }),
        apiToken,
      )
        .then((response) => {
          if (response.status !== 200) {
            throw new Error("Error uploading opening book metadata!");
          }
          return response.text();
        })
        .then((book_id) => {
          const fd = new FormData();
          fd.set("file", file!);
          return FormDataCallDirectAsUser(
            `/opening-books/content?book_id=${book_id}`,
            "POST",
            fd,
            apiToken,
          );
        })
        .then((response) => {
          if (response.status !== 204) {
            throw new Error("Error uploading opening book data!");
          }
          successCallback();
          setUploadStatus("uploaded");
        })
        .catch(() => {
          errorCallback();
          setUploadStatus("error");
        })
        .finally(() => {
          refreshBookCallbackRef.current();
          resetUploadIconTimeoutRef.current = window.setTimeout(() => {
            setUploadStatus("none");
          }, 5000);
        });
    }, 1000);
  }

  return (
    <tr>
      <th scope="row">Upload new book</th>
      <td>
        <input
          className="form-control"
          type="file"
          id="fileInput"
          accept=".zip,.pgn,.epd"
          disabled={uploadStatus == "uploading"}
          onChange={(e) => {
            const file = e.target.files!.item(0);
            setFile(file);
          }}
        />
      </td>
      <td>
        <button
          type="button"
          className={`btn btn-sm btn-${(() => {
            return {
              none: "secondary",
              uploading: "secondary",
              uploaded: "success",
              error: "danger",
            }[uploadStatus];
          })()}`}
          disabled={file == null || uploadStatus == "uploading"}
          onClick={uploadOpeningBook}
        >
          {(() => {
            switch (uploadStatus) {
              case "none":
                return <i className="bi-upload" />;
              case "uploading":
                return (
                  <div
                    className="spinner-border spinner-border-sm"
                    role="status"
                  >
                    <span className="visually-hidden">Uploading...</span>
                  </div>
                );
              case "uploaded":
                return <i className="bi-check-lg" />;
              case "error":
                return <i className="bi-x-lg" />;
            }
          })()}
        </button>
      </td>
    </tr>
  );
}
