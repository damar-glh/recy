import {CONFIG} from "../config/upload.config";

export class ValidationUtils {
    static checkFileSize(file) {
        return file.size <= CONFIG.maxFileSize;
    }

    static checkFileType(file) {
        return CONFIG.allowedFileTypes.includes(file.type);
    }
}