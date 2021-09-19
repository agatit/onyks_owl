import { toNamespacedPath } from "path/posix";
import { toast } from "react-toastify";
import { ToastPosition } from "react-toastify/dist/types";

export enum NotificationType {
  SUCCESS,
  INFO,
  WARNING,
  ERROR,
}

export interface NotificationParams {
  text: string;
  position?: ToastPosition;
  type?: NotificationType;
}

export default function getNotification(params: NotificationParams) {
  switch (params.type) {
    case NotificationType.SUCCESS: {
      toast.success(params.text, { position: params.position });
      break;
    }
    case NotificationType.INFO: {
      toast.info(params.text, { position: params.position });
      break;
    }
    case NotificationType.WARNING: {
      toast.warning(params.text, { position: params.position });
      break;
    }
    case NotificationType.ERROR: {
      toast.error(params.text, { position: params.position });
      break;
    }
  }
}
