import pickle
import sys

def inspect_model(file_path):
    try:
        with open(file_path, 'rb') as f:
            model_data = pickle.load(f)
            
        with open('model_inspection.txt', 'w', encoding='utf-8') as out_f:
            out_f.write(f"Model data type: {type(model_data)}\n")
            if isinstance(model_data, dict):
                out_f.write("Keys available in model:\n")
                for k, v in model_data.items():
                    out_f.write(f" - {k}: {type(v)}\n")
            elif hasattr(model_data, '__dict__'):
                out_f.write("Attributes available in model:\n")
                for k in dir(model_data):
                    if not k.startswith('_'):
                        out_f.write(f" - {k}\n")
            else:
                out_f.write(f"Model is not a dictionary and has no __dict__. Value is: {repr(model_data)[:200]}\n")
    except Exception as e:
        import traceback
        with open('model_inspection.txt', 'w', encoding='utf-8') as out_f:
            traceback.print_exc(file=out_f)
            out_f.write("\nYou might need to use joblib or install specific libraries used in Colab.")

if __name__ == '__main__':
    inspect_model('recommendation_model.pkl')
