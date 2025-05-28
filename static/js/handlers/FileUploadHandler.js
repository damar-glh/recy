import {CONFIG} from "../config/upload.config";
import {ValidationUtils} from "../utils/ValidationUtils";

export class FileUploadHandler {
    constructor() {
        this.uploadForm = document.getElementById('uploadForm');
        this.fileInput = document.getElementById('fileInput');
        this.counter = document.getElementById('counter');

        this.initializeEventListeners();
    }

    initializeEventListeners() {
        this.uploadForm.addEventListener('change', (e) => this.handleFileChange(e));
        this.uploadForm.addEventListener('dragover', (e) => this.handleDragOver(e));
        this.uploadForm.addEventListener('dragleave', (e) => this.handleDragLeave(e));
        this.uploadForm.addEventListener('drop', (e) => this.handleDrop(e));
    }

    validateFile(file) {
        const isValidType = ValidationUtils.checkFileType(file);
        const isValidSize = ValidationUtils.checkFileSize(file);

        if (!isValidSize || !isValidType) {
            this.showError();
            return false;
        }
        return true;
    }

    showError() {
        this.counter.classList.remove(...CONFIG.cssClasses.normal);
        this.counter.classList.add(...CONFIG.cssClasses.error);
    }

    handleFileChange(e) {
        e.preventDefault();
        const file = e.target.files[0];
        this.processFile(file);
    }

    handleDragOver(e) {
        e.preventDefault();
        this.uploadForm.classList.add(...CONFIG.cssClasses.dragOver);
    }

    handleDragLeave(e) {
        e.preventDefault();
        this.uploadForm.classList.remove(...CONFIG.cssClasses.dragOver);
    }

    handleDrop(e) {
        e.preventDefault();
        this.uploadForm.classList.remove(...CONFIG.cssClasses.dragOver);

        const file = e.dataTransfer.files[0];
        const newDataTransfer = new DataTransfer();
        newDataTransfer.items.add(file);
        this.fileInput.files = newDataTransfer.files;

        this.processFile(file);
    }

    processFile(file) {
        try {
            if (this.validateFile(file)) {
                this.uploadForm.submit();
            }
        } catch (error) {
            console.error('Error processing file:', error);
        }
    }
}