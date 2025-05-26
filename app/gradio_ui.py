import gradio as gr
import httpx
import os
import mimetypes  

# Define the FastAPI base URL
FASTAPI_BASE_URL = "http://127.0.0.1:8000"

# Asynchronous client for making HTTP requests
client = httpx.AsyncClient()



async def gradio_upload_image(image_file_obj):
    """
    Handles the image upload from Gradio to the FastAPI backend.

    This asynchronous function takes an image file object (typically a file path
    provided by Gradio's gr.File component), uploads it to the FastAPI endpoint
    `/identity_cards/save_file/`, and returns the path where the image was saved
    on the server, along with a status message.

    Parameters
    ----------
    image_file_obj : str or None
        The path to the uploaded image file provided by Gradio. If no file was
        uploaded, this will be None.

    Returns
    -------
    tuple
        A tuple containing:
        - str or None: The full path to the saved image file on the server if
          upload was successful, otherwise None.
        - str: A status message indicating the success or failure of the upload,
          including any error details.

    Raises
    ------
    httpx.HTTPStatusError
        If the FastAPI backend returns an HTTP error status (4xx or 5xx).
    FileNotFoundError
        If the temporary file provided by Gradio cannot be found.
    Exception
        For any other unexpected errors during the upload process.

    Notes
    -----
    This function internally uses `httpx.AsyncClient` to perform an
    asynchronous POST request to the FastAPI backend. It infers the filename
    and content type from the provided file path. Existing PNG files in the
    upload directory on the server are deleted before a new file is saved by
    the FastAPI backend.
    """
    if image_file_obj is None:
        return None, "Please upload an image."

    file_path = image_file_obj
    filename = os.path.basename(file_path)
    # mimetype, To tell the receiving application (in our case, your FastAPI server) what kind of data it's about to receive, so it knows how to handle it correctly.
    # Hey FastAPI, I'm sending you some data. By the way, this data's MIME type is image/png.
    content_type, _ = mimetypes.guess_type(filename)
    if not content_type:
        content_type = "application/octet-stream"

    try:
        with open(file_path, "rb") as f:
            files = {"file": (filename, f, content_type)}
            # You can not give file_path directly without opening it, as httpx needs to read the actual binary content of the file.
            response = await client.post(
                f"{FASTAPI_BASE_URL}/identity_cards/save_file/", files=files
            )
            response.raise_for_status()

            result = response.json()
            saved_file_path = result.get("message")

            return saved_file_path, f"Image uploaded to: {saved_file_path}"

    except httpx.HTTPStatusError as e:
        return (
            None,
            f"Error uploading image (HTTP Status {e.response.status_code}): {e.response.text}",
        )
    except FileNotFoundError:
        return (
            None,
            f"Error: The uploaded file was not found at {file_path}. It might have been temporary.",
        )
    except Exception as e:
        return None, f"An unexpected error occurred during upload: {e}"


async def gradio_get_extracted_results():
    """
    Fetches and formats the latest OCR inference results from the FastAPI backend.

    This asynchronous function makes an HTTP GET request to the FastAPI endpoint
    `/identity_cards/show_inference_results/`. This endpoint is expected to
    perform the OCR on the latest uploaded image and return the extracted data.
    The function then formats the received data into a human-readable string
    suitable for display in a Gradio Textbox.

    Parameters
    ----------
    None

    Returns
    -------
    str
        A multi-line string containing the formatted OCR results, where each
        extracted field (e.g., ID Number, Name, Birth Date) is displayed on a
        new line with a descriptive label. If no data is available or an error
        occurs, an appropriate error message is returned.

    Raises
    ------
    httpx.HTTPStatusError
        If the FastAPI backend returns an HTTP error status (4xx or 5xx).
    Exception
        For any other unexpected errors during the data retrieval or parsing process.

    Notes
    -----
    The FastAPI endpoint `/identity_cards/show_inference_results/` should
    internally ensure that the OCR process is executed on the most recently
    uploaded image file. This function relies on the FastAPI response
    containing specific keys like 'identity_number', 'surname', 'name',
    and 'birth_date'.
    """
    try:
        response = await client.get(
            f"{FASTAPI_BASE_URL}/identity_cards/show_inference_results/"
        )
        response.raise_for_status()

        result = response.json()

        formatted_result = (
            f"*ID Number*: {result.get('identity_number', 'N/A')}\n"
            f"*Surname*: {result.get('surname', 'N/A')}\n"
            f"*Name*: {result.get('name', 'N/A')}\n"
            f"*Birth Date*: {result.get('birth_date', 'N/A')}\n"
        )

        return formatted_result

    except httpx.HTTPStatusError as e:
        return f"Error getting inference results (HTTP Status {e.response.status_code}): {e.response.text}"
    except Exception as e:
        return f"An unexpected error occurred getting results: {e}"


async def gradio_save_results_to_db():
    """
    Triggers the FastAPI backend to save the latest OCR inference results to the database.

    This asynchronous function makes an HTTP POST request to the FastAPI endpoint
    `/identity_cards/save_inference_results/`. This endpoint is responsible for
    reading the most recently generated JSON inference result (on the server-side)
    and persisting that data into the application's database. The function then
    returns a status message indicating the success or failure of the save operation.

    Parameters
    ----------
    None

    Returns
    -------
    str
        A success message including details of the saved record (e.g., ID,
        Identity Number, Name, Surname) if the operation was successful.
        If an error occurs, an appropriate error message is returned.

    Raises
    ------
    httpx.HTTPStatusError
        If the FastAPI backend returns an HTTP error status (4xx or 5xx).
    Exception
        For any other unexpected errors during the database save process.

    Notes
    -----
    This function relies on the FastAPI backend having successfully performed OCR
    and stored the results in a temporary JSON file via a previous call to
    `/identity_cards/show_inference_results/`. The backend endpoint handles
    the database session management and data insertion.
    """
    try:
        response = await client.post(
            f"{FASTAPI_BASE_URL}/identity_cards/save_inference_results/"
        )
        response.raise_for_status()

        result = response.json()

        return (
            f"Results saved to database successfully!\n"
            f"ID: {result.get('id', 'N/A')}\n"
            f"Identity Number: {result.get('identity_number', 'N/A')}\n"
            f"Name-Surname: {result.get('name', 'N/A')} {result.get('surname', 'N/A')}\n"
            f"Birth Date: {result.get('birth_date', 'N/A')}\n"
        )

    except httpx.HTTPStatusError as e:
        return f"Error saving results to database (HTTP Status {e.response.status_code}): {e.response.text}"
    except Exception as e:
        return f"An unexpected error occurred saving to DB: {e}"


async def gradio_get_all_saved_results():
    """
    Fetches and formats all identity card records stored in the database.

    This asynchronous function makes an HTTP GET request to the FastAPI endpoint
    `/identity_cards/get_inference_results`. This endpoint retrieves all saved
    identity card entries from the database. The function then processes the
    received list of records, formatting each entry into a user-friendly string
    for display in a Gradio Textbox, separated by a visual delimiter.

    Parameters
    ----------
    None

    Returns
    -------
    str
        A multi-line string where each line represents a saved identity card
        record, detailing its ID, Identity Number, Name, Surname, Birth Date,
        and Created At. Records are separated by '---' for readability.
        Returns "No results saved yet." if the database contains no entries,
        or an error message if the retrieval fails.

    Raises
    ------
    httpx.HTTPStatusError
        If the FastAPI backend returns an HTTP error status (4xx or 5xx).
    Exception
        For any other unexpected errors during the data retrieval or formatting process.

    Notes
    -----
    This function expects the FastAPI backend to return a list of dictionaries,
    each conforming to the `IdentityCardResponse` schema, containing keys such
    as 'id', 'identity_number', 'surname', 'name', 'birth_date', and
    'created_at'.
    """
    try:
        response = await client.get(
            f"{FASTAPI_BASE_URL}/identity_cards/get_inference_results"
        )
        response.raise_for_status()

        results = response.json()

        if not results:
            return "No results saved yet."

        formatted_results = []
        for card in results:
            card_str = (
                f"ID: {card.get('id', 'N/A')}, "
                f"Identity Number: {card.get('identity_number', 'N/A')}, "
                f"Name: {card.get('name', 'N/A')} {card.get('surname', 'N/A')}, "
                f"Birth Date: {card.get('birth_date', 'N/A')}, "
                f"Created At: {card.get('created_at', 'N/A')}"
            )
            formatted_results.append(card_str)

        return "\n---\n".join(formatted_results)

    except httpx.HTTPStatusError as e:
        return f"Error retrieving all results (HTTP Status {e.response.status_code}): {e.response.text}"
    except Exception as e:
        return f"An unexpected error occurred retrieving all results: {e}"


def create_gradio_ui():
    """
    Constructs and returns the complete Gradio Blocks interface for the Identity Card OCR application.

    This function defines the layout and interactive components of the web-based
    user interface. It sets up sections for image upload and display, OCR
    result extraction, saving results to the database, and viewing all saved
    records. All UI interactions are wired to corresponding asynchronous
    functions (e.g., `gradio_upload_image`, `gradio_get_extracted_results`)
    that communicate with the FastAPI backend.

    Parameters
    ----------
    None

    Returns
    -------
    gradio.Blocks
        A Gradio Blocks object representing the complete user interface. This
        object can then be mounted onto a FastAPI application.

    See Also
    --------
    gradio_upload_image : Handles image upload and display.
    gradio_get_extracted_results : Fetches and displays OCR results.
    gradio_save_results_to_db : Saves OCR results to the database.
    gradio_get_all_saved_results : Retrieves and displays all saved records.

    Notes
    -----
    The UI components are arranged using `gr.Blocks`, `gr.Row`, and `gr.Column`
    for a structured layout. Event listeners like `.upload()` and `.click()`
    are used to trigger backend interactions based on user actions.
    `type="filepath"` for `gr.File` and `gr.Image` ensures that file paths
    are handled for display and processing.
    """
    with gr.Blocks() as demo:
        gr.Markdown("# Turkish Identity Card Scan")

        with gr.Row():
            with gr.Column():
                image_input = gr.File(
                    label="Upload Image (PNG files)",
                    file_types=[".png"],
                    type="filepath",
                )
                print(image_input)
                uploaded_image_display = gr.Image(
                    label="Uploaded Image", type="filepath", show_label=True
                )
                upload_status = gr.Textbox(label="Upload Status", interactive=False)

                image_input.upload(
                    gradio_upload_image,
                    inputs=[image_input],
                    outputs=[uploaded_image_display, upload_status],
                )

            with gr.Column():
                extract_button = gr.Button("See Extracted Results")
                extracted_results_output = gr.Textbox(
                    label="Extracted Information", interactive=False, lines=8
                )
                extract_button.click(
                    gradio_get_extracted_results,
                    inputs=[],
                    outputs=[extracted_results_output],
                )

                save_button = gr.Button("Save Results to Database")
                save_status_output = gr.Textbox(label="Save Status", interactive=False)
                save_button.click(
                    gradio_save_results_to_db, inputs=[], outputs=[save_status_output]
                )

                gr.Markdown("---")
                gr.Markdown("### View All Saved Results")
                view_all_button = gr.Button("View All Identity Cards")
                all_results_output = gr.Textbox(
                    label="All Saved Identity Cards", interactive=False, lines=10
                )

                view_all_button.click(
                    gradio_get_all_saved_results,
                    inputs=[],
                    outputs=[all_results_output],
                )
    return demo


if __name__ == "__main__":
    print(f"Gradio UI attempting to connect to FastAPI at {FASTAPI_BASE_URL}")
    demo = create_gradio_ui()
    demo.launch()
