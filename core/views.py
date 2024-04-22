import os
import pandas as pd
import datetime
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import base64
import json

@csrf_exempt
def ContrastExcelFiles(request): 
    """
    Compare two Excel files and save the combined new data and statistics.
    
    Request format:
    {
      "data1": "path_to_file1",
      "data2": "path_to_file2"
    }
    
    Response format:
    {
      "Status": 1 or -1,
      "Message": "Success message or error message",
      "CombinedNewDataPath": "path_to_combined_new_data.xlsx",
      "ComparisonStatisticsPath": "path_to_comparison_statistics.xlsx"
    }
    """
    print("ContrastCsvFiles Started: "+str(datetime.datetime.now()))
    fileDate = str(datetime.datetime.now())
    try:
        # Extract data paths from JSON request
        dic = json.loads(request.body)

        path_file1 = dic['data1']
        path_file2 = dic['data2']

        if not (path_file1 and path_file2):
            return JsonResponse({'Status': -1, 'Message': 'Missing file paths', 'path_file1':str(path_file1),'path_file2':str(path_file2)})

        # Read Excel files
        df1 = pd.read_excel(path_file1)
        df2 = pd.read_excel(path_file2)

        # Ensure columns are in the same order and structure as df1
        df2 = df2[df1.columns]

        # Find new data from df2 compared to df1
        new_in_df2 = df2[~df2.isin(df1.to_dict(orient='list')).all(axis=1)]

        # Find new data from df1 compared to df2
        new_in_df1 = df1[~df1.isin(df2.to_dict(orient='list')).all(axis=1)]

        # Combine the new data from both files
        combined_new_data = pd.concat([new_in_df1, new_in_df2])

        # Save combined new data to a new Excel file
        output_dir = os.path.join(os.getcwd(), 'output')
        os.makedirs(output_dir, exist_ok=True)
        combined_new_data_path = os.path.join(output_dir, f"{fileDate}_combined_new_data.xlsx")
        combined_new_data.to_excel(combined_new_data_path, index=False)

        # Save statistics to an Excel file
        initial_stats = pd.DataFrame({
            "Statistic": ["Rows in df1", "Rows in df2", "Unique rows in df1", "Unique rows in df2"],
            "Value": [len(df1), len(df2), df1.nunique(), df2.nunique()]
        })

        final_stats = pd.DataFrame({
            "Statistic": ["New rows in df1", "New rows in df2", "Total new rows"],
            "Value": [len(new_in_df1), len(new_in_df2), len(combined_new_data)]
        })

        comparison_statistics_path = os.path.join(output_dir, f"{fileDate}_comparison_statistics.xlsx")
        with pd.ExcelWriter(comparison_statistics_path) as writer:
            initial_stats.to_excel(writer, sheet_name='Initial Statistics', index=False)
            final_stats.to_excel(writer, sheet_name='Final Statistics', index=False)

        # Construct response
        response = {
            "Status": 1,
            "Message": "Files compared successfully.",
            "CombinedNewDataPath": combined_new_data_path,
            "ComparisonStatisticsPath": comparison_statistics_path
        }
        print("ContrastCsvFiles Ended: "+str(datetime.datetime.now())) 
        return JsonResponse(response)
    
    except Exception as ex:
        print('Exception:', str(ex))
        print("ContrastCsvFiles Ended: "+str(datetime.datetime.now())) 
        return JsonResponse({'Status': -1, 'Message': 'Exception occurred', 'ExceptionDetails': str(ex)})

@csrf_exempt
def ContrastCsvFiles(request):
    print("ContrastCsvFiles Started: "+str(datetime.datetime.now()))
    fileDate = str(datetime.datetime.now()) 
    """
    Compare two CSV files and save the combined new data and statistics.
    
    Request format:
    {
      "data1": "path_to_file1",
      "data2": "path_to_file2"
    }
    
    Response format:
    {
      "Status": 1 or -1,
      "Message": "Success message or error message",
      "CombinedNewDataPath": "path_to_combined_new_data.csv",
      "ComparisonStatisticsPath": "path_to_comparison_statistics.csv"
    }
    """
    try:
        # Extract data paths from JSON request
        dic = json.loads(request.body)

        path_file1 = dic['data1']
        path_file2 = dic['data2']

        if not (path_file1 and path_file2):
            return JsonResponse({'Status': -1, 'Message': 'Missing file paths', 'path_file1':str(path_file1),'path_file2':str(path_file2)})

        # Read CSV files
        df1 = pd.read_csv(path_file1)
        df2 = pd.read_csv(path_file2)

        # Ensure columns are in the same order and structure as df1
        df2 = df2[df1.columns]

        # Find new data from df2 compared to df1
        new_in_df2 = df2[~df2.isin(df1.to_dict(orient='list')).all(axis=1)]

        # Find new data from df1 compared to df2
        new_in_df1 = df1[~df1.isin(df2.to_dict(orient='list')).all(axis=1)]

        # Combine the new data from both files
        combined_new_data = pd.concat([new_in_df1, new_in_df2])

        # Save combined new data to a new CSV file
        output_dir = os.path.join(os.getcwd(), 'output')
        os.makedirs(output_dir, exist_ok=True)
        combined_new_data_path = os.path.join(output_dir, f"{fileDate}_combined_new_data.csv")
        combined_new_data.to_csv(combined_new_data_path, index=False)

        # Save statistics to a CSV file
        initial_stats = pd.DataFrame({
            "Statistic": ["Rows in df1", "Rows in df2", "Unique rows in df1", "Unique rows in df2"],
            "Value": [len(df1), len(df2), df1.nunique(), df2.nunique()]
        })

        final_stats = pd.DataFrame({
            "Statistic": ["New rows in df1", "New rows in df2", "Total new rows"],
            "Value": [len(new_in_df1), len(new_in_df2), len(combined_new_data)]
        })

        comparison_statistics_path = os.path.join(output_dir, f"{fileDate}_comparison_statistics.csv")
        with open(comparison_statistics_path, 'w') as writer:
            initial_stats.to_csv(writer, index=False, header=True)
            final_stats.to_csv(writer, index=False, header=False, mode='a')

        # Construct response
        response = {
            "Status": 1,
            "Message": "CSV Files compared successfully.",
            "CombinedNewDataPath": combined_new_data_path,
            "ComparisonStatisticsPath": comparison_statistics_path
        }
        print("ContrastCsvFiles Ended: "+str(datetime.datetime.now())) 
        return JsonResponse(response)
    
    except Exception as ex:
        print('Exception:', str(ex))
        print("ContrastCsvFiles Ended: "+str(datetime.datetime.now())) 
        return JsonResponse({'Status': -1, 'Message': 'Exception occurred', 'ExceptionDetails': str(ex)})

@csrf_exempt
def ContrastLargeCsvFiles(request):
    print("ContrastCsvFiles Started: " + str(datetime.datetime.now()))
    
    try:
        # Extract data paths from JSON request
        dic = json.loads(request.body)

        path_file1 = dic['data1']
        path_file2 = dic['data2']

        if not (path_file1 and path_file2):
            return JsonResponse({
                'Status': -1,
                'Message': 'Missing file paths',
                'path_file1': str(path_file1),
                'path_file2': str(path_file2)
            })

        # Read CSV files with low_memory=False to suppress DtypeWarning
        df1 = pd.read_csv(path_file1, low_memory=False)
        df2 = pd.read_csv(path_file2, low_memory=False)

        # Ensure columns are in the same order and structure as df1
        df2 = df2[df1.columns]

        # Find new data from df2 compared to df1
        new_in_df2 = df2[~df2.isin(df1.to_dict(orient='list')).all(axis=1)]

        # Find new data from df1 compared to df2
        new_in_df1 = df1[~df1.isin(df2.to_dict(orient='list')).all(axis=1)]

        # Combine the new data from both files
        combined_new_data = pd.concat([new_in_df1, new_in_df2])

        # Save combined new data and statistics
        output_dir = os.path.join(os.getcwd(), 'output')
        os.makedirs(output_dir, exist_ok=True)
        file_date = str(datetime.datetime.now())
        
        # Save combined new data to a new CSV file
        combined_new_data_path = os.path.join(output_dir, f"{file_date}_combined_new_data.csv")
        combined_new_data.to_csv(combined_new_data_path, index=False)

        # Create statistics DataFrames
        initial_stats = pd.DataFrame({
            "Statistic": ["Rows in df1", "Rows in df2", "Unique rows in df1", "Unique rows in df2"],
            "Value": [len(df1), len(df2), df1.nunique(), df2.nunique()]
        })

        final_stats = pd.DataFrame({
            "Statistic": ["New rows in df1", "New rows in df2", "Total new rows"],
            "Value": [len(new_in_df1), len(new_in_df2), len(combined_new_data)]
        })

        # Save statistics to a CSV file
        comparison_statistics_path = os.path.join(output_dir, f"{file_date}_comparison_statistics.csv")
        with open(comparison_statistics_path, 'w') as writer:
            initial_stats.to_csv(writer, index=False, header=True)
            final_stats.to_csv(writer, index=False, header=False, mode='a')

        # Construct response
        response = {
            "Status": 1,
            "Message": "CSV Files compared successfully.",
            "CombinedNewDataPath": combined_new_data_path,
            "ComparisonStatisticsPath": comparison_statistics_path
        }
        
        print("ContrastCsvFiles Ended: " + str(datetime.datetime.now())) 
        return JsonResponse(response)

    except FileNotFoundError as fnf_error:
        print('FileNotFoundError:', str(fnf_error))
        print("ContrastCsvFiles Ended: " + str(datetime.datetime.now())) 
        return JsonResponse({
            'Status': -1,
            'Message': 'File not found',
            'ExceptionDetails': str(fnf_error)
        })

    except Exception as ex:
        print('Exception:', str(ex))
        print("ContrastCsvFiles Ended: " + str(datetime.datetime.now())) 
        return JsonResponse({
            'Status': -1,
            'Message': 'Exception occurred',
            'ExceptionDetails': str(ex)
        })

@csrf_exempt
def ContrastLargeCsvFile1(request):
    print("ContrastCsvFiles Started: " + str(datetime.datetime.now()))
    
    try:
        # Extract data paths from JSON request
        dic = json.loads(request.body)

        path_file1 = dic['data1']
        path_file2 = dic['data2']

        if not (path_file1 and path_file2):
            return JsonResponse({
                'Status': -1,
                'Message': 'Missing file paths',
                'path_file1': str(path_file1),
                'path_file2': str(path_file2)
            })

        # Read CSV files with low_memory=False to suppress DtypeWarning
        df1 = pd.read_csv(path_file1, low_memory=False)
        df2 = pd.read_csv(path_file2, low_memory=False)

        # Ensure columns are in the same order and structure as df1
        df2 = df2[df1.columns]

        # Find new data from df2 compared to df1
        new_in_df2 = df2[~df2.isin(df1.to_dict(orient='list')).all(axis=1)]

        # Find new data from df1 compared to df2
        new_in_df1 = df1[~df1.isin(df2.to_dict(orient='list')).all(axis=1)]

        # Combine the new data from both files
        combined_new_data = pd.concat([new_in_df1, new_in_df2])

        # Save combined new data to a new CSV file
        output_dir = os.path.join(os.getcwd(), 'output')
        os.makedirs(output_dir, exist_ok=True)
        file_date = str(datetime.datetime.now())
        combined_new_data_path = os.path.join(output_dir, f"{file_date}_combined_new_data.csv")
        combined_new_data.to_csv(combined_new_data_path, index=False)

        # Calculate and include statistics in the response
        initial_stats = {
            "Rows in df1": len(df1),
            "Rows in df2": len(df2),
            "Unique rows in df1": df1.nunique().to_dict(),
            "Unique rows in df2": df2.nunique().to_dict()
        }

        final_stats = {
            "New rows in df1": len(new_in_df1),
            "New rows in df2": len(new_in_df2),
            "Total new rows": len(combined_new_data)
        }

        # Construct response
        response = {
            "Status": 1,
            "Message": "CSV Files compared successfully.",
            "CombinedNewDataPath": combined_new_data_path,
            "InitialStatistics": initial_stats,
            "FinalStatistics": final_stats
        }
        
        print("ContrastCsvFiles Ended: " + str(datetime.datetime.now())) 
        return JsonResponse(response)

    except FileNotFoundError as fnf_error:
        print('FileNotFoundError:', str(fnf_error))
        print("ContrastCsvFiles Ended: " + str(datetime.datetime.now())) 
        return JsonResponse({
            'Status': -1,
            'Message': 'File not found',
            'ExceptionDetails': str(fnf_error)
        })

    except Exception as ex:
        print('Exception:', str(ex))
        print("ContrastCsvFiles Ended: " + str(datetime.datetime.now())) 
        return JsonResponse({
            'Status': -1,
            'Message': 'Exception occurred',
            'ExceptionDetails': str(ex)
        })

""" """ 
@csrf_exempt
def ContrastLargeCsvFile(request):
    print("ContrastCsvFiles Started: " + str(datetime.datetime.now()))
    
    # Expected headers for the first 12 columns
    expected_headers = [
    "MANDT", "OTYPE", "OBJID", "PLVAR", "RSIGN", "RELAT",
    "ISTAT", "PRIOX", "BEGDA", "ENDDA", "VARYF", "SEQNR"
    ]
    
    try:
        # Extract data paths from JSON request
        dic = json.loads(request.body)

        path_file1 = dic['data1']
        path_file2 = dic['data2']

        if not (path_file1 and path_file2):
            return JsonResponse({
                'Status': -1,
                'Message': 'Missing file paths',
                'path_file1': str(path_file1),
                'path_file2': str(path_file2)
            })

        # Define data types for columns causing warnings
        dtype_dict = {
            'RSIGN': str,
            'PRIOX': str,
            'BEGDA': str,
            'ITXNR': str
        }

        # Read CSV files with specified data types and low_memory=False
        df1 = pd.read_csv(path_file1, dtype=dtype_dict, low_memory=False)
        df2 = pd.read_csv(path_file2, dtype=dtype_dict, low_memory=False)

        # Ensure columns are in the same order and structure as df1
        df2 = df2[df1.columns]

        # Find new data from df2 compared to df1
        new_in_df2 = df2[~df2.isin(df1.to_dict(orient='list')).all(axis=1)]

        # Find new data from df1 compared to df2
        new_in_df1 = df1[~df1.isin(df2.to_dict(orient='list')).all(axis=1)]

        # Combine the new data from both files
        combined_new_data = pd.concat([new_in_df1, new_in_df2])

        # Extract first 12 columns for update and insert CSV files
        combined_new_data_first_12 = combined_new_data[expected_headers]

        # Save combined new data to a new CSV file
        output_dir = os.path.join(os.getcwd(), 'output')
        os.makedirs(output_dir, exist_ok=True)
        file_date = str(datetime.datetime.now())
        combined_new_data_path = os.path.join(output_dir, f"{file_date}_combined_new_data.csv")
        combined_new_data_first_12.to_csv(combined_new_data_path, index=False)

        # Save update and insert CSV files
        update_path = os.path.join(output_dir, f"{file_date}_update.csv")
        insert_path = os.path.join(output_dir, f"{file_date}_insert.csv")

        new_in_df1[expected_headers].to_csv(update_path, index=False)
        new_in_df2[expected_headers].to_csv(insert_path, index=False)

        # Calculate and include statistics in the response
        initial_stats = {
            "Rows in df1": len(df1),
            "Rows in df2": len(df2)
            #"Unique rows in df1": df1.nunique().to_dict(),
            #"Unique rows in df2": df2.nunique().to_dict()
        }

        final_stats = {
            "New rows in df1": len(new_in_df1),
            "New rows in df2": len(new_in_df2),
            "Total new rows": len(combined_new_data_first_12)
        }

        # Construct response
        response = {
            "Status": 1,
            "Message": "CSV Files compared successfully.",
            "CombinedNewDataPath": combined_new_data_path,
            "UpdateCsvPath": update_path,
            "InsertCsvPath": insert_path,
            "InitialStatistics": initial_stats,
            "FinalStatistics": final_stats
        }
        
        print("ContrastCsvFiles Ended: " + str(datetime.datetime.now())) 
        return JsonResponse(response)

    except FileNotFoundError as fnf_error:
        print('FileNotFoundError:', str(fnf_error))
        print("ContrastCsvFiles Ended: " + str(datetime.datetime.now())) 
        return JsonResponse({
            'Status': -1,
            'Message': 'File not found',
            'ExceptionDetails': str(fnf_error)
        })

    except Exception as ex:
        print('Exception:', str(ex))
        print("ContrastCsvFiles Ended: " + str(datetime.datetime.now())) 
        return JsonResponse({
            'Status': -1,
            'Message': 'Exception occurred',
            'ExceptionDetails': str(ex)
        })