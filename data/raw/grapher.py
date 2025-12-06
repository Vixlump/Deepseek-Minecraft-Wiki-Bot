import os
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

def get_json_file_sizes(folder_path):
    """
    Get all JSON files in the folder and their sizes in KB
    """
    json_files = []
    file_sizes_kb = []
    
    # Check if folder exists
    if not os.path.exists(folder_path):
        print(f"Error: Folder '{folder_path}' does not exist.")
        return [], []
    
    # Get all JSON files in the folder
    for file_name in os.listdir(folder_path):
        if file_name.lower().endswith('.json'):
            file_path = os.path.join(folder_path, file_name)
            
            # Get file size in bytes and convert to KB
            file_size_bytes = os.path.getsize(file_path)
            file_size_kb = file_size_bytes / 1024
            
            json_files.append(file_name)
            file_sizes_kb.append(file_size_kb)
    
    return json_files, file_sizes_kb

def process_top_files(json_files, file_sizes_kb, top_n=20):
    """
    Process files to get top N largest and group the rest as 'Other'
    """
    # Combine files and sizes into tuples and sort by size (descending)
    file_data = list(zip(json_files, file_sizes_kb))
    file_data.sort(key=lambda x: x[1], reverse=True)
    
    # Separate top N files and the rest
    top_files_data = file_data[:top_n]
    remaining_files_data = file_data[top_n:]
    
    # Calculate total size of remaining files
    other_total_size = sum(size for _, size in remaining_files_data)
    
    # Prepare data for plotting
    if remaining_files_data:
        # Create labels and sizes for top files + "Other"
        labels = [f"{name}" for name, _ in top_files_data] + ["Other"]
        sizes = [size for _, size in top_files_data] + [other_total_size]
        
        # Count remaining files for the Other category
        other_count = len(remaining_files_data)
    else:
        # If there are 20 or fewer files, just show all
        labels = [f"{name}" for name, _ in top_files_data]
        sizes = [size for _, size in top_files_data]
        other_count = 0
    
    return labels, sizes, other_count, len(remaining_files_data)

def create_top20_bar_graph(json_files, file_sizes_kb, output_path="json_top20_sizes.png"):
    """
    Create a bar graph showing top 20 largest JSON files and Other category
    """
    if not json_files:
        print("No JSON files found to plot.")
        return
    
    # Process files to get top 20 + Other
    labels, sizes, other_count, remaining_files = process_top_files(json_files, file_sizes_kb, top_n=20)
    
    # Create the plot with larger size for better readability
    plt.figure(figsize=(16, 10))
    
    # Create color palette - different color for "Other" category
    colors = []
    for i, label in enumerate(labels):
        if label == "Other":
            colors.append('gray')  # Gray for "Other" category
        else:
            # Use a colormap for individual files
            colors.append(plt.cm.viridis(i / max(20, len(labels) - 1)))
    
    bars = plt.bar(labels, sizes, color=colors)
    
    # Customize the plot
    total_files = len(json_files)
    if other_count > 0:
        title = f'Top 20 Largest JSON Files ({total_files} total files, {other_count} in "Other")'
    else:
        title = f'All JSON Files ({total_files} total files)'
    
    plt.title(title, fontsize=18, fontweight='bold', pad=20)
    plt.xlabel('JSON Files', fontsize=14)
    plt.ylabel('File Size (KB)', fontsize=14)
    
    # Rotate x-axis labels for better readability
    plt.xticks(rotation=45, ha='right', fontsize=10)
    plt.yticks(fontsize=11)
    
    # Add value labels on top of each bar
    for bar, value in zip(bars, sizes):
        height = bar.get_height()
        if value > 0:  # Only add label if value is positive
            label_text = f'{value:.1f} KB'
            if bar.get_x() + bar.get_width()/2 == bars[-1].get_x() + bars[-1].get_width()/2 and labels[-1] == "Other":
                # Add count to Other category
                label_text = f'{value:.1f} KB\n({other_count} files)'
            
            plt.text(bar.get_x() + bar.get_width()/2, height + (max(sizes)*0.01), 
                    label_text, ha='center', va='bottom', fontsize=9, 
                    bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.8))
    
    # Add horizontal grid lines
    plt.grid(axis='y', alpha=0.3, linestyle='--')
    
    # Add a legend for the Other category
    if other_count > 0:
        from matplotlib.patches import Patch
        legend_elements = [
            Patch(facecolor='gray', edgecolor='black', label=f'"Other" Category ({other_count} files, {sum(sizes[-1:]):.1f} KB total)')
        ]
        plt.legend(handles=legend_elements, loc='upper right', fontsize=11)
    
    # Adjust layout to prevent label cutoff
    plt.tight_layout()
    
    # Save the plot
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"Top 20 graph saved as: {output_path}")
    
    # Show the plot
    plt.show()
    
    return other_count, remaining_files

def create_pie_chart_top20(json_files, file_sizes_kb, output_path="json_top20_pie.png"):
    """
    Create a pie chart showing the distribution of top 20 files vs Others
    """
    if not json_files:
        print("No JSON files found to plot.")
        return
    
    # Process files to get top 20 + Other
    labels, sizes, other_count, _ = process_top_files(json_files, file_sizes_kb, top_n=20)
    
    # Create the plot
    plt.figure(figsize=(14, 10))
    
    # Create a list of labels with sizes
    display_labels = []
    for label, size in zip(labels, sizes):
        if label == "Other":
            display_labels.append(f'Other\n{size:.1f} KB\n({other_count} files)')
        else:
            display_labels.append(f'{label}\n{size:.1f} KB')
    
    # Create colors - gray for Other
    colors = []
    for i, label in enumerate(labels):
        if label == "Other":
            colors.append('lightgray')
        else:
            colors.append(plt.cm.Set3(i / 20))
    
    # Create the pie chart
    wedges, texts, autotexts = plt.pie(sizes, labels=display_labels, colors=colors,
                                       autopct='%1.1f%%', startangle=90,
                                       pctdistance=0.85, textprops={'fontsize': 9})
    
    # Draw a circle in the center to make it a donut chart
    centre_circle = plt.Circle((0, 0), 0.70, fc='white')
    fig = plt.gcf()
    fig.gca().add_artist(centre_circle)
    
    # Add a title
    total_files = len(json_files)
    if other_count > 0:
        title = f'File Size Distribution: Top 20 vs Others\n({total_files} total files)'
    else:
        title = f'File Size Distribution\n({total_files} total files)'
    
    plt.title(title, fontsize=16, fontweight='bold', pad=20)
    
    # Equal aspect ratio ensures that pie is drawn as a circle
    plt.axis('equal')
    
    # Adjust layout
    plt.tight_layout()
    
    # Save the plot
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"Pie chart saved as: {output_path}")
    
    # Show the plot
    plt.show()

def print_detailed_summary(json_files, file_sizes_kb, other_count, remaining_files):
    """
    Print a detailed summary of the JSON files
    """
    if not json_files:
        return
    
    print("\n" + "="*60)
    print("DETAILED JSON FILES SUMMARY")
    print("="*60)
    
    total_files = len(json_files)
    total_size_kb = sum(file_sizes_kb)
    avg_size_kb = total_size_kb / total_files
    
    # Sort files by size
    sorted_data = sorted(zip(json_files, file_sizes_kb), key=lambda x: x[1], reverse=True)
    
    print(f"\n📊 OVERVIEW:")
    print(f"   Total JSON files: {total_files}")
    print(f"   Total size: {total_size_kb:.2f} KB")
    print(f"   Average size: {avg_size_kb:.2f} KB")
    
    print(f"\n🏆 TOP 20 LARGEST FILES:")
    for i, (file_name, size_kb) in enumerate(sorted_data[:20], 1):
        percentage = (size_kb / total_size_kb) * 100
        print(f"   {i:2d}. {file_name[:40]:40s} {size_kb:8.2f} KB ({percentage:5.1f}%)")
    
    if other_count > 0:
        other_files = sorted_data[20:]
        other_total = sum(size for _, size in other_files)
        other_percentage = (other_total / total_size_kb) * 100
        avg_other_size = other_total / other_count if other_count > 0 else 0
        
        print(f"\n📦 OTHER CATEGORY ({other_count} files):")
        print(f"   Total size of Other files: {other_total:.2f} KB ({other_percentage:.1f}%)")
        print(f"   Average size of Other files: {avg_other_size:.2f} KB")
        
        # Show the largest file in the Other category
        if other_files:
            largest_other = other_files[0]
            print(f"   Largest file in Other: {largest_other[0]} ({largest_other[1]:.2f} KB)")
    
    print(f"\n📈 SIZE RANGES:")
    print(f"   Largest file: {max(file_sizes_kb):.2f} KB")
    print(f"   Smallest file: {min(file_sizes_kb):.2f} KB")
    
    # Calculate quartiles
    sorted_sizes = sorted(file_sizes_kb)
    q1 = sorted_sizes[total_files // 4]
    median = sorted_sizes[total_files // 2]
    q3 = sorted_sizes[3 * total_files // 4]
    
    print(f"   Median size: {median:.2f} KB")
    print(f"   25th percentile: {q1:.2f} KB")
    print(f"   75th percentile: {q3:.2f} KB")
    print("="*60)

def main():
    """
    Main function to run the script
    """
    # Get folder path from user or use current directory
    folder_path = input("Enter the folder path (or press Enter for current directory): ").strip()
    
    if not folder_path:
        folder_path = os.getcwd()
    
    print(f"Scanning folder: {folder_path}")
    
    # Get JSON file information
    json_files, file_sizes_kb = get_json_file_sizes(folder_path)
    
    if not json_files:
        print(f"No JSON files found in '{folder_path}'")
        return
    
    # Create output file names based on folder name
    folder_name = os.path.basename(folder_path) or "current"
    
    # Create graphs
    output_bar = f"json_top20_{folder_name}.png"
    output_pie = f"json_top20_pie_{folder_name}.png"
    
    print(f"\nFound {len(json_files)} JSON files")
    
    # Create bar chart and get Other category info
    other_count, remaining_files = create_top20_bar_graph(json_files, file_sizes_kb, output_bar)
    
    # Create pie chart
    create_pie_chart_top20(json_files, file_sizes_kb, output_pie)
    
    # Print detailed summary
    print_detailed_summary(json_files, file_sizes_kb, other_count, remaining_files)
    
    print(f"\n✅ Graphs generated successfully!")
    print(f"   Bar chart: {output_bar}")
    print(f"   Pie chart: {output_pie}")
    print(f"\n📁 Total files analyzed: {len(json_files)}")
    if other_count > 0:
        print(f"   Top 20 largest files shown individually")
        print(f"   {other_count} smaller files grouped as 'Other'")

if __name__ == "__main__":
    main()