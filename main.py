from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from typing import List
from dotenv import load_dotenv
import search
import prompt_templates
from flashrank import Ranker, RerankRequest
import os
import numpy as np  # Add numpy import for type checking

cache_directory = os.path.join(os.path.dirname(__file__), ".model_cache")
os.makedirs(cache_directory, exist_ok=True)

# Revert to the previously working reranker model due to download issues with bge-reranker-large
ranker = Ranker(model_name="ms-marco-MultiBERT-L-12", cache_dir=cache_directory)

load_dotenv()


# cors origins
# cors origins
origins = [
    "*"  # Allow all origins
]


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class QueryRequest(BaseModel):
    query: str
    top_n: int = 10
    groq: bool = True


import os
from fastapi import UploadFile
GROQ_API_KEY=os.getenv("GROQ_API_KEY")
if GROQ_API_KEY is None:
    print("No GROQ_API_KEY found in environment variables")
    exit(1)



groqHandler = search.groqHandler(api_key=GROQ_API_KEY, template=prompt_templates.words_to_product)
wqs = search.WeaviateQueryService(collection="CleanedProducts", groqHandler=groqHandler, target_vector="name_master_sub_art_col_use_seas_gender")
image_search = search.ImageSearch(wqs = wqs)

@app.get("/")
async def read_root():
    return '<h1> Welcome to the Semantic Search Engine </h1><br> <h2> Please use the <a href="http://localhost:8888/search/">/search/</a> endpoint to search for products </h2>'



@app.post("/text_search")
async def search_item(query: QueryRequest):

    if not query.query:
        return JSONResponse(status_code=400, content=jsonable_encoder({"error": "Query not found"}))

    limit = query.top_n
    groq_simplify = query.groq
    original_query = query.query # Keep original query for reranking


    print(f" \n\n\n Got query : {original_query}\n\n\n")

    # Perform initial search
    # Assuming wqs.get_results returns a list of full product dictionaries
    initial_results = wqs.get_results(query=original_query, limit=limit, groq_llama_simplfy=groq_simplify, print_responses_name=True)

    # Check if the response is a list as expected
    if not isinstance(initial_results, list):
        print(f"Error: Expected a list from wqs.get_results, but got {type(initial_results)}")
        return JSONResponse(status_code=500, content=jsonable_encoder({"error": "Internal search error: Unexpected result format"}))

    if not initial_results: # Handle empty results case
        return JSONResponse(status_code=200, content=jsonable_encoder([]))

    # --- Reranking Logic ---
    # Create a lookup map for full product details by ID
    results_map = {}
    for i, item in enumerate(initial_results):
         # Ensure item is a dict and has an ID
        if isinstance(item, dict):
            item_id = item.get("productId", item.get("id", i)) # Prioritize 'productId' if available
            item['productId'] = item_id # Ensure 'productId' key exists for consistency
            results_map[item_id] = item
        else:
             # Handle unexpected item format if necessary
             print(f"Warning: Skipping unexpected item format in initial results: {item}")


    # Prepare passages for flashrank: List[Dict] with 'id' and 'text'
    passages_for_rerank = []
    for item_id, item_data in results_map.items():
        product_text = item_data.get("productDisplayName") or item_data.get("name") or item_data.get("text", "")
        passages_for_rerank.append({"id": item_id, "text": product_text})


    # Check if there are passages to rerank
    if not passages_for_rerank:
         print("Warning: No valid passages found to rerank.")
         # Return initial results if nothing to rerank (or handle as error)
         return JSONResponse(status_code=200, content=jsonable_encoder(initial_results))


    # Use the formatted list for reranking
    rerankrequest = RerankRequest(query=original_query, passages=passages_for_rerank)

    try:
        reranked_ids_scores = ranker.rerank(rerankrequest) # This returns [{'id': ..., 'score': ...}]
    except Exception as e:
        print(f"Error during reranking: {e}")
        # Return an error response or potentially the original un-reranked results
        return JSONResponse(status_code=500, content=jsonable_encoder({"error": f"Reranking failed: {e}"}))

    # --- Construct Final Ordered Results ---
    final_ordered_results = []
    for reranked_item in reranked_ids_scores:
        item_id = reranked_item.get("id")
        if item_id in results_map:
            full_product_details = results_map[item_id]
            # Optionally add the reranker score to the result
            full_product_details['rerank_score'] = float(reranked_item['score']) if isinstance(reranked_item.get('score'), (np.float32, np.float64)) else reranked_item.get('score')
            final_ordered_results.append(full_product_details)
        else:
            print(f"Warning: ID {item_id} from reranker not found in initial results map.")


    # Return the full product details, ordered by the reranker
    return JSONResponse(status_code=200, content=jsonable_encoder(final_ordered_results))



@app.post("/image-search/")
async def search_image(image: UploadFile = File(...), top_n: int = 30):
    # Process the image
    image_data = await image.read()

    # Assuming image_search.get_results returns a list of results
    response = image_search.get_results(image_data=image_data, top_n=top_n)

    # Add similar check and formatting if reranking is desired for image search too
    # For now, returning direct results as per original code

    return response
    # return response


@app.get('/recommends')
async def recommend_products():
    response = wqs.get_recommends()
    return response



# @app.get("/images/{image_name}")
# async def get_image(image_name: str):
#     file_path = f"images/{image_name}.jpg"
#     return FileResponse(file_path)