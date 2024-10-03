
from pyzbar.pyzbar import decode
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

def scan_qr_code():
    cap = cv2.VideoCapture(0)
    
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame")
            break
        
        # Convert frame to RGB for tkinter
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(img)
        imgtk = ImageTk.PhotoImage(image=img)
        lbl.imgtk = imgtk
        lbl.configure(image=imgtk)
        
        # Detect and decode QR codes
        for barcode in decode(frame):
            barcode_data = barcode.data.decode('utf-8')
            barcode_type = barcode.type
            
            # Draw rectangle around QR code
            pts = barcode.polygon
            if len(pts) == 4:
                pts = [(int(pt.x), int(pt.y)) for pt in pts]
                cv2.polylines(frame, [np.array(pts, dtype=np.int32)], isClosed=True, color=(0, 255, 0), thickness=3)
                
            # Show the result
            messagebox.showinfo("QR Code Detected", f"Decoded Data: {barcode_data}")
            cap.release()
            cv2.destroyAllWindows()
            return

        # Break the loop with 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()

# Create the GUI using Tkinter
root = tk.Tk()
root.title("QR Code Scanner")

lbl = tk.Label(root)
lbl.pack(padx=10, pady=10)

btn = tk.Button(root, text="Scan QR Code", command=scan_qr_code, font=("Arial", 16), bg="green", fg="white")
btn.pack(pady=20)

# Quit button
quit_btn = tk.Button(root, text="Quit", command=root.quit, font=("Arial", 16), bg="red", fg="white")
quit_btn.pack(pady=10)

root.mainloop()
