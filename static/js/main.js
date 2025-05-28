console.log('main.js');
import { FileUploadHandler } from './handlers/FileUploadHandler';

document.addEventListener('DOMContentLoaded', () => {
    new FileUploadHandler();
})