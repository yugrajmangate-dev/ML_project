import pickle
import pandas as pd
import numpy as np

class Recommender:
    def __init__(self, model_path):
        with open(model_path, 'rb') as f:
            model_data = pickle.load(f)
            
        self.user_similarity_df = model_data['user_similarity_df']
        self.user_item_matrix_binary = model_data['user_item_matrix_binary']
        self.products_df = model_data['products_df']
        self.cosine_sim_content = model_data['cosine_sim_content']
        self.indices = model_data['indices']

    def recommend_collaborative(self, customer_id, num_recommendations=5):
        try:
            # Ensure proper type if dealing with floats vs strings
            if customer_id not in self.user_similarity_df.index:
                try: customer_id = float(customer_id)
                except: pass
                if customer_id not in self.user_similarity_df.index:
                    return {"error": "Customer ID not found in dataset."}
                
            # Get top similar users
            similar_users = self.user_similarity_df[customer_id].sort_values(ascending=False).index[1:6]
            
            # Get items bought by target user
            target_user_items = set(self.user_item_matrix_binary.loc[customer_id][self.user_item_matrix_binary.loc[customer_id] > 0].index)
            
            recommendations = []
            for sim_user in similar_users:
                sim_user_items = set(self.user_item_matrix_binary.loc[sim_user][self.user_item_matrix_binary.loc[sim_user] > 0].index)
                new_items = sim_user_items - target_user_items
                recommendations.extend(list(new_items))
                
            unique_recs = []
            for r in recommendations:
                if r not in unique_recs:
                    unique_recs.append(r)
            
            if not unique_recs:
                return {"message": "No new collaborative recommendations found (too similar).", "products": []}
                
            top_n_ids = unique_recs[:num_recommendations]
            
            # Form product results
            rec_products = self.products_df[self.products_df['StockCode'].isin(top_n_ids)].drop_duplicates(subset=['StockCode'])
            
            result = []
            for _, row in rec_products.iterrows():
                result.append({
                    "id": str(row['StockCode']),
                    "name": str(row['Description'])
                })
                
            return {"products": result}
        except Exception as e:
            return {"error": str(e)}

    def recommend_content(self, product_query, num_recommendations=5):
        try:
            # Check by index either by StockCode or Description
            if product_query in self.indices.index:
                idx = self.indices[product_query]
            else:
                # search description
                matches = self.products_df[self.products_df['Description'].str.contains(product_query, case=False, na=False)]
                if matches.empty:
                    return {"error": "Product not found in dataset."}
                
                stock_code = matches.iloc[0]['StockCode']
                if stock_code not in self.indices.index:
                    return {"error": "Product found in DB but not mapped in similarity matrix."}
                idx = self.indices[stock_code]
            
            # Handle duplicates in indices if there are any
            if isinstance(idx, pd.Series):
                idx = idx.iloc[0]
                
            sim_scores = list(enumerate(self.cosine_sim_content[int(idx)]))
            sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
            
            sim_scores = sim_scores[1:num_recommendations+1]
            item_indices = [i[0] for i in sim_scores]
            
            # Get stockcodes using indices.
            # Convert indices Series back to get StockCode from int index
            # Series maps StockCode -> Index, so we invert it
            inv_map = {v: k for k, v in self.indices.items() if isinstance(v, (int, np.integer))}
            if not inv_map:
                # Invert handles duplicates and might not be bulletproof, here's a safer way
                stock_codes = [self.indices.index[i] for i in item_indices]
            else:
                stock_codes = [inv_map.get(i) for i in item_indices]
            
            rec_products = self.products_df[self.products_df['StockCode'].isin(stock_codes)].drop_duplicates(subset=['StockCode'])
            
            result = []
            for _, row in rec_products.iterrows():
                result.append({
                    "id": str(row['StockCode']),
                    "name": str(row['Description'])
                })
                
            return {"products": result}        
        except Exception as e:
            return {"error": str(e)}
