import { copyTextToClipboard } from "@/scripts/Utils/Clipboard";
import { NotificationType, notify } from "@/components/Notifications";
import React from "react";

export default function CopyToClipboardButton({
  text,
  disabled,
}: {
  text: string;
  disabled?: boolean;
}): JSX.Element {
  const [icon, setIcon] = React.useState("clipboard");
  const resetIconTimeoutRef = React.useRef<number | null>();

  return (
    <button
      className="btn btn-outline-secondary"
      type="button"
      title="Copy to clipboard"
      disabled={disabled == null ? false : disabled}
      onClick={() => {
        if (resetIconTimeoutRef.current) {
          window.clearTimeout(resetIconTimeoutRef.current);
        }
        if (copyTextToClipboard(text)) {
          notify("Successfully copied to clipboard!", NotificationType.Success);
          setIcon("clipboard-check");
        } else {
          notify("Failed to copy to clipboard!", NotificationType.Error);
          setIcon("clipboard-x");
        }
        resetIconTimeoutRef.current = window.setTimeout(() => {
          setIcon("clipboard");
        }, 5000);
      }}
    >
      <i className={`bi-${icon}`} />
    </button>
  );
}
